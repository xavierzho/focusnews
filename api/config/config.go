package config

// Properties ...
type Properties struct {
	Port           string `env:"NEWS_PORT" env-default:"5200"`
	Host           string `env:"NEWS_HOST" env-default:"localhost"`
	LogLevel       string `env:"LOG_LEVEL" env-default:"ERROR"`
	MongoURI       string `env:"mongoURI" env-default:"mongodb://localhost:27017"`
	NewsDatabase   string `env:"NEWS_DATABASE" env-default:"news"`
	NewsCollection string `env:"NEWS_COLLECTION" env-default:"summary"`
}
