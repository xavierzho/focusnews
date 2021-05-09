package routers

import (
	"context"
	"database/sql"

	"go.mongodb.org/mongo-driver/mongo/options"

	"go.mongodb.org/mongo-driver/mongo"
)

type (
	// CollectionAPI Mongodb CURD API
	CollectionAPI interface {
		InsertOne(ctx context.Context, document interface{}, opts ...*options.InsertOneOptions) (*mongo.InsertOneResult, error)
		Find(ctx context.Context, filter interface{}, opts ...*options.FindOptions) (*mongo.Cursor, error)
		FindOne(ctx context.Context, filter interface{}, opts ...*options.FindOneOptions) *mongo.SingleResult
		UpdateOne(ctx context.Context, filter interface{}, update interface{}, opts ...*options.UpdateOptions) (*mongo.UpdateResult, error)
		DeleteOne(ctx context.Context, filter interface{}, opts ...*options.DeleteOptions) (*mongo.DeleteResult, error)
	}
	DBHandler struct {
		Mongodb *mongo.Database
		MySQL   *sql.Conn
	}
	ListRequestData struct {
		PageNum  int    `form:"page_num" json:"page_num"`
		PageSize int    `form:"page_size" json:"page_size"`
		SortKey  string `form:"sort_key" json:"sort_key"`
		Status   int    `form:"status" json:"status"`
		Keyword  string `form:"keyword" json:"keyword"`
	}
	ListResponse struct {
		Status  int         `json:"status"`
		Message string      `json:"message"`
		Total   int         `json:"total"`
		Data    interface{} `json:"data"`
		Error   string      `json:"error"`
	}
	Response struct {
		Status  int         `json:"status"`
		Message string      `json:"message"`
		Data    interface{} `json:"data"`
		Error   string      `json:"error"`
	}
)
