package main

import (
	"api/config"
	"api/handlers"
	"context"
	"flag"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"syscall"

	"github.com/ilyakaznacheev/cleanenv"
	"github.com/labstack/echo/v4"
	"github.com/sevlyar/go-daemon"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var (
	e         = echo.New()
	newsDB    *mongo.Database
	newsCol   *mongo.Collection
	cfg       config.Properties
	ErrSignal = fmt.Errorf("signal valid")
	s         = &http.Server{}
)

func init() {

	//fmt.Printf("%+v", cfg)
	if err := cleanenv.ReadEnv(&cfg); err != nil {
		e.Logger.Fatalf("Configuration cannot be read: %+v", err)
	}
	//init mongodb connect
	c, err := mongo.Connect(context.Background(), options.Client().ApplyURI(cfg.MongoURI))
	if err != nil {
		e.Logger.Fatalf("Unable to connect to database : %+v", err)
	}
	newsDB = c.Database(cfg.NewsDatabase)
	newsCol = newsDB.Collection(cfg.NewsCollection)
}

func server() {
	nh := &handlers.NewsHandler{Col: newsCol}
	// news routers
	e.GET("/news", nh.GetNewsS)
	e.GET("/news/:id", nh.GetNews)
	e.POST("/news", nh.CreateNews)
	e.PUT("/news/:id", nh.ModifyNews)
	e.DELETE("/news/:id", nh.DeleteNews)
	//middleware

	// server start
	e.Logger.Fatal(e.Start(fmt.Sprintf("%s:%s", cfg.Host, cfg.Port)))
}
func main() {
	os.Args[0], _ = filepath.Abs(os.Args[0])
	signals := flag.String("s", "", "send signal to daemon")
	daemon.AddCommand(daemon.StringFlag(signals, "stop"), syscall.SIGTERM, Shutdown)
	daemon.AddCommand(daemon.StringFlag(signals, "reload"), syscall.SIGHUP, Reload)

	flag.Parse()
	dmn := &daemon.Context{
		PidFileName: "./log/pinksale.pid",
		PidFilePerm: 0644,
		LogFileName: "./log/pinksale.log",
		LogFilePerm: 0640,
		WorkDir:     "/",
		Umask:       027,
	}
	if len(daemon.ActiveFlags()) > 0 {
		d, err := dmn.Search()
		if err != nil {
			fmt.Println("Unable send signal to the daemon:", err)
		}
		_ = daemon.SendCommands(d)
		return
	}
	child, err := dmn.Reborn()
	if err != nil {
		fmt.Println("reborn:", err)
	}
	if child != nil {
		return
	}
	defer dmn.Release()

	// business logic
	go server()

	err = daemon.ServeSignals()
	if err != nil {
		fmt.Println("Error:", err)
	}
}
func Shutdown(sig os.Signal) error {
	if sig != syscall.SIGTERM {
		return ErrSignal
	}
	//common.LOG.Info("system exit later...")
	os.Exit(0)
	return nil
}
func Reload(sig os.Signal) error {
	if sig != syscall.SIGHUP {
		return ErrSignal
	}
	s.RegisterOnShutdown(func() {
		path := os.Args[0]
		cmd := exec.Command(path, os.Args[1:]...)
		cmd.Stdout = os.Stdout
		cmd.Stdin = os.Stdin
		cmd.Stderr = os.Stderr
		cmd.Env = os.Environ()
		err := cmd.Start()
		if err != nil {
			fmt.Println("reload failed")

		}
		fmt.Println("system reload success ...")
	})
	return s.Shutdown(context.Background())
}
