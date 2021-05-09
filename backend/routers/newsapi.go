package routers

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strconv"

	"go.mongodb.org/mongo-driver/mongo"

	"github.com/labstack/echo/v4"
	"github.com/labstack/gommon/log"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo/options"
	"gopkg.in/go-playground/validator.v9"
)

var (
	v       = validator.New()
	colName = "summary"
)

// News Abstract the news
type News struct {
	ID        primitive.ObjectID `json:"id,omitempty" bson:"_id"`
	Title     string             `json:"title,omitempty" bson:"title" validate:"required,max=256"`
	Published string             `json:"published,omitempty" bson:"published" validate:"required"`
	Source    string             `json:"source,omitempty" bson:"source" validate:"required"`
	Content   interface{}        `json:"content,omitempty" bson:"content"`
	Link      string             `json:"link,omitempty" bson:"link" validate:"required,url"`
	NavLink   interface{}        `json:"nav_link,omitempty" bson:"nav_link" validate:"url"`
	NavName   interface{}        `json:"nav_name,omitempty" bson:"nav_name"`
	NewsID    interface{}        `json:"news_id,omitempty" bson:"news_id"`
	Images    interface{}        `json:"images,omitempty" bson:"images"`
}

// NewsValidator validator bind method
type NewsValidator struct {
	validator *validator.Validate
}

// Validate Validate upload data
func (nv *NewsValidator) Validate(i interface{}) error {
	return nv.validator.Struct(i)
}

// findManyNews Find the news real method in db
func findManyNews(ctx context.Context, query url.Values, collection *mongo.Collection) ([]News, error) {
	var (
		newsList []News
		//Note:Not declared in the loop!!
		limit int64 = 20
		skip  int64 = 0
		sort  int64 = -1
	)
	fmt.Println(query)
	limit, err := strconv.ParseInt(query.Get("limit"), 10, 64)
	skip, err = strconv.ParseInt(query.Get("skip"), 10, 64)
	sort, err = strconv.ParseInt(query.Get("limit"), 10, 64)
	if err != nil {
		return nil, echo.NewHTTPError(http.StatusInternalServerError, "Params is no Number")
	}

	//fmt.Println("filter:", filter)
	// 调用CollectionAPI接口
	opts := options.Find().SetSort(bson.M{"published": sort}).SetLimit(limit).SetSkip(skip).SetMax(100)
	cursor, err := collection.Find(ctx, bson.D{}, opts)
	if err != nil {
		log.Errorf("Unable to find the news :\"%+v\"", err)
		return nil, echo.NewHTTPError(http.StatusInternalServerError, "Unable to find the news")
	}

	if err := cursor.All(ctx, &newsList); err != nil {
		log.Errorf("Unable to read the cursor :%+v", err)
		return nil, echo.NewHTTPError(http.StatusInternalServerError, "Unable to read the cursor")
	}
	defer cursor.Close(ctx)
	return newsList, nil
}

// GetNewsS get one news API
func (nh *DBHandler) GetNewsS(c echo.Context) error {
	col := nh.Mongodb.Collection(colName)
	news, err := findManyNews(context.Background(), c.QueryParams(), col)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "Unable to find news list")
	}
	return c.JSON(http.StatusOK, Response{
		Status: 1,
		Data:   news,
	})
}

//findOneNews Find the news real method in db
func findOneNews(ctx context.Context, query string, collection *mongo.Collection) (News, error) {
	var news News
	docId, err := primitive.ObjectIDFromHex(query)
	if err != nil {
		return news, echo.NewHTTPError(http.StatusBadRequest, "The Id valid")
	}
	res := collection.FindOne(ctx, bson.M{"_id": docId})
	if err := res.Decode(&news); err != nil {
		log.Errorf("Unable to Serialization to the struct：%+v", err)
		return news, echo.NewHTTPError(http.StatusInternalServerError, "Unable to Serialization")
	}
	return news, nil
}

// GetNews get one news
func (nh *DBHandler) GetNews(c echo.Context) error {
	col := nh.Mongodb.Collection(colName)
	news, err := findOneNews(context.Background(), c.Param("id"), col)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "Unable to find news")
	}
	return c.JSON(http.StatusOK, Response{
		Status:  1,
		Data:    news,
		Message: "success to query a news!",
	})
}

// insertNews create news real method in db
func insertNews(ctx context.Context, newsList []News, collection CollectionAPI) ([]interface{}, error) {
	var insertIds []interface{}
	var exists News
	for _, news := range newsList {
		// find the news title and source exists in db
		res := collection.FindOne(ctx, bson.M{"title": news.Title, "source": news.Source})
		if err := res.Decode(&exists); err == nil {
			return nil, echo.NewHTTPError(http.StatusBadRequest, fmt.Sprintf("Title:%s is exists", exists.Title))
		}
		news.ID = primitive.NewObjectID()
		insertId, err := collection.InsertOne(ctx, news)
		if err != nil {
			return nil, echo.NewHTTPError(http.StatusInternalServerError, fmt.Sprintf("Has something error with:%#v", news))
		}
		insertIds = append(insertIds, insertId.InsertedID)
	}
	return insertIds, nil
}

// CreateNews create news api
func (nh *DBHandler) CreateNews(c echo.Context) error {
	var newsList []News
	c.Echo().Validator = &NewsValidator{v}
	if err := c.Bind(&newsList); err != nil {
		log.Printf("Unable to bind :%v", err)
		return echo.NewHTTPError(http.StatusBadRequest, "Unable to parse request payload")
	}
	for _, news := range newsList {
		if err := c.Validate(news); err != nil {
			log.Printf("Unable to validate the product:%+v;%v", news, err)
			return echo.NewHTTPError(http.StatusBadRequest, "Unable to validate request payload")
		}
	}
	col := nh.Mongodb.Collection(colName)
	IDs, err := insertNews(context.Background(), newsList, col)
	if err != nil {
		return err
	}
	return c.JSON(http.StatusOK, Response{
		Status:  1,
		Data:    IDs,
		Message: fmt.Sprintf("Success insert %d News", len(IDs)),
	})
}

// updateNews update news real method
func updateNews(ctx context.Context, id string, reqBody io.ReadCloser, collection CollectionAPI) (News, error) {
	var news News
	//find news exists in db
	docID, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		log.Errorf("Cannot convert to objectId :%+v", err)
		return news, echo.NewHTTPError(http.StatusInternalServerError, "Cannot convert to objectId") // 500 err code
	}
	filter := bson.M{"_id": docID}
	res := collection.FindOne(ctx, filter)
	if err := res.Decode(&news); err != nil {
		return news, echo.NewHTTPError(http.StatusBadRequest, "Cannot decode the news")
	}
	//parse then reqBody
	if err := json.NewDecoder(reqBody).Decode(&news); err != nil {
		return news, echo.NewHTTPError(http.StatusInternalServerError, "Connot decode the reqBody")
	}
	// validate the news
	if err := v.Struct(news); err != nil {
		return news, echo.NewHTTPError(http.StatusInternalServerError, "Unable to validate request payload")
	}
	// insert into db
	_, err = collection.UpdateOne(ctx, filter, bson.M{"$set": news})
	if err != nil {
		return news, echo.NewHTTPError(http.StatusInternalServerError, "Cannot update to database")
	}
	return news, nil
}

// ModifyNews update news api
func (nh *DBHandler) ModifyNews(c echo.Context) error {
	col := nh.Mongodb.Collection(colName)
	news, err := updateNews(context.Background(), c.Param("id"), c.Request().Body, col)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "Unable to modify the news")
	}
	return c.JSON(http.StatusOK, Response{
		Status:  1,
		Data:    news,
		Message: "Success to update News",
	})
}

// deleteNews delete news real method
func deleteNews(ctx context.Context, id string, collection CollectionAPI) (int64, error) {
	var news News
	//find the news exists in db
	docID, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		log.Errorf("Cannot convert to objectId :%+v", err)
		return 0, echo.NewHTTPError(http.StatusInternalServerError, "The id valid") // 500 err code
	}
	res := collection.FindOne(ctx, bson.M{"_id": docID})
	if err := res.Decode(&news); err != nil {
		return 0, echo.NewHTTPError(http.StatusBadRequest, "The news don't exists")
	}
	// del form db
	delRes, err := collection.DeleteOne(ctx, bson.M{"_id": docID})
	if err != nil {
		return 0, echo.NewHTTPError(http.StatusInternalServerError, "Unable to delete the news")
	}
	return delRes.DeletedCount, nil
}

// DeleteNews delete news api
func (nh *DBHandler) DeleteNews(c echo.Context) error {
	col := nh.Mongodb.Collection(colName)
	delCount, err := deleteNews(context.Background(), c.Param("id"), col)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "Unable to delete the news")
	}
	return c.JSON(http.StatusOK, Response{
		Status:  1,
		Message: fmt.Sprintf("Delete %d news", delCount),
	})
}
