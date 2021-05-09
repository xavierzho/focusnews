package dbs

import (
	"context"
	"os"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func InitMongo() (*mongo.Client, error) {
	client, err := mongo.Connect(context.TODO(), options.Client().ApplyURI(os.Getenv("mongoURI")))
	if err != nil {
		return nil, err
	}
	// check connection
	if err := client.Ping(context.TODO(), nil); err != nil {
		return nil, err
	}
	return client, nil
}
