package main

import (
	"api/config"
	"api/handlers"
	"context"
	"fmt"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	"github.com/ilyakaznacheev/cleanenv"
	"github.com/labstack/echo/v4"
)

var (
	e = echo.New()

	newsDB  *mongo.Database
	newsCol *mongo.Collection
	cfg     config.Properties
)

func init() {

	fmt.Printf("%+v", cfg)
	if err := cleanenv.ReadEnv(&cfg); err != nil {
		e.Logger.Fatalf("Configuration cannot be read: %+v", err)
	}
	c, err := mongo.Connect(context.Background(), options.Client().ApplyURI(cfg.MongoURI))
	if err != nil {
		e.Logger.Fatalf("Unable to connect to database : %+v", err)
	}
	newsDB = c.Database(cfg.NewsDatabase)
	newsCol = newsDB.Collection(cfg.NewsCollection)

}
func main() {

	nh := &handlers.NewsHandler{Col: newsCol}
	// news routers
	e.GET("/news", nh.GetNews)
	e.GET("/news/:id", nh.GetNew)
	e.POST("/news", nh.CreateNews)
	e.PUT("/news/:id", nh.ModifyNews)
	e.DELETE("/news/:id", nh.DeleteNews)
	//middleware

	// server start
	e.Logger.Fatal(e.Start(fmt.Sprintf("%s:%s", cfg.Host, cfg.Port)))
}
