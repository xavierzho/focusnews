package response

type JsonResp struct {
	Status   int         `json:"status"`
	Data     interface{} `json:"data"`
	Message  string      `json:"message"`
	NextPage string      `json:"next_page"`
	PrePage  string      `json:"pre_page"`
}
