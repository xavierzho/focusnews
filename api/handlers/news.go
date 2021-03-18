package handlers

import (
	"api/dbinterface"
	"api/response"
	"context"
	"net/http"
	"net/url"

	"github.com/labstack/gommon/log"

	"gopkg.in/go-playground/validator.v9"

	"github.com/labstack/echo/v4"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

var (
	v = validator.New()
)

type News struct {
	ID        primitive.ObjectID `json:"_id" bson:"_id"`
	Title     string             `json:"title" bson:"title"`
	Published string             `json:"published" bson:"published"`
	Source    string             `json:"source" bson:"source"`
	Content   bson.A             `json:"content" bson:"content"`
	Link      string             `json:"link" bson:"link"`
	NavLink   string             `json:"nav_link" bson:"nav_link"`
	NavName   string             `json:"nav_name" bson:"nav_name"`
	NewsID    string             `json:"news_id" bson:"news_id"`
	Images    bson.A             `json:"images" bson:"images"`
}
type NewsHandler struct {
	Col dbinterface.CollectionAPI
}
type NewsValidator struct {
	validator *validator.Validate
}

func (nv *NewsValidator) Validate(i interface{}) error {
	return nv.validator.Struct(i)
}
func findNews(ctx context.Context, query url.Values, collection dbinterface.CollectionAPI) ([]News, error) {
	var news []News
	filter := make(map[string]interface{})
	for k, v := range query {
		filter[k] = v[0]
	}
	// 调用CollectionAPI
	cursor, err := collection.Find(ctx, bson.M(filter))
	if err != nil {
		log.Errorf("Unable to find the news :%+v", err)
	}
	err = cursor.All(ctx, &news)
	if err != nil {
		log.Errorf("Unable to read the cursor :%+v", err)
		return news, echo.NewHTTPError(http.StatusInternalServerError, "Unable to read the cursor")
	}
	return news, nil
}
func (nh *NewsHandler) GetNews(c echo.Context) error {
	news, err := findNews(context.Background(), c.QueryParams(), nh.Col)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "Unable to find products")
	}
	return c.JSON(http.StatusOK, response.JsonResp{
		Status: 1,
		Data: news,
	})
}
//todo
func (nh *NewsHandler) GetNew(c echo.Context) error {

	return c.JSON(http.StatusOK, response.JsonResp{
		Status: 1,
		Data: 12,
		Message: "success to query a news!",
	})
}
//todo
func (nh *NewsHandler) CreateNews(c echo.Context) error {
	return c.JSON(http.StatusOK, "")
}
//todo
func (nh *NewsHandler) ModifyNews(c echo.Context) error {
	return c.JSON(http.StatusOK, "")
}
//todo
func (nh *NewsHandler) DeleteNews(c echo.Context) error {
	return c.JSON(http.StatusOK, "")
}
