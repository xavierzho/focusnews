package middlewares

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func Writer(fp string) io.Writer {
	file, err := os.Open(fp)
	if err != nil {
		fmt.Println("Failed to open file")
	}
	return bufio.NewWriter(file)
}
