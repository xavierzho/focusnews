package main

import (
	"encoding/json"
	"fmt"
	"focus/config"
	"focus/dbs"
	"focus/routers"
	"io/ioutil"
	"net"

	"github.com/labstack/echo/v4/middleware"

	"github.com/spf13/viper"

	"github.com/labstack/echo/v4"
)

func main() {
	app := echo.New()
	// 初始化配置
	if err := config.InitConfig(""); err != nil {
		app.Logger.Fatal("Init config error!")
	}
	// 初始化日志配置
	//logPath := viper.GetString("log.path")
	app.Use(middleware.LoggerWithConfig(middleware.DefaultLoggerConfig))
	//初始化mongodb
	client, err := dbs.InitMongo()
	if err != nil {
		app.Logger.Fatal(err)
	}
	db := client.Database(viper.GetString("mongo.db"))
	h := &routers.DBHandler{
		Mongodb: db,
	}
	anonymousGroup := app.Group("")
	{
		// news routers
		anonymousGroup.GET("/news", h.GetNewsS).Name = "manyNews"
		anonymousGroup.GET("/news/:id", h.GetNews).Name = "oneNews"

	}
	AuthGroup := app.Group("auth")
	AuthGroup.Use(middleware.JWTWithConfig(middleware.JWTConfig{
		SigningKey:  []byte(viper.GetString("jwt.secret")),
		TokenLookup: "header:x-auth-token",
	}))
	{
		AuthGroup.POST("/news", h.CreateNews).Name = "createNews"
		AuthGroup.PUT("/news/:id", h.ModifyNews).Name = "updateNews"
		AuthGroup.DELETE("/news/:id", h.DeleteNews).Name = "deleteNews"
	}
	// 服务运行
	host := viper.GetString("server.host")
	port := viper.GetString("server.port")
	address := net.JoinHostPort(host, port)
	// 输出所有的路由信息
	data, err := json.MarshalIndent(app.Routes(), "", "  ")
	if err != nil {
		fmt.Println("Marshal Error", err)
	}
	if err := ioutil.WriteFile("routes.json", data, 0644); err != nil {
		fmt.Println("Write File err", err)
	}

	app.Logger.Fatal(app.Start(address))

}
