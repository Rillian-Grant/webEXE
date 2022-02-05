package main

import (
	"embed"
	"fmt"
	"io/fs"
	"log"
	"net"
	"net/http"
	"os/exec"
	"runtime"
)

//go:embed www
var embeddedFiles embed.FS

var PORT string = "8080"

func main() {
	r := http.NewServeMux()

	embeddedFiles, err := fs.Sub(embeddedFiles, "www")
	if err != nil {
		panic(err)
	}
	r.Handle("/", http.FileServer(http.FS(embeddedFiles)))

	log.Println("Opening socket")
	l, err := net.Listen("tcp", "localhost:"+PORT)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Opening browser")
	openBrowser("http://localhost:" + PORT)

	log.Println("Starting server")
	err = http.Serve(l, r)
	if err != nil {
		panic(err)
	}
}

func openBrowser(url string) {
	var err error

	switch runtime.GOOS {
	case "linux":
		err = exec.Command("xdg-open", url).Start()
	case "windows":
		err = exec.Command("rundll32", "url.dll,FileProtocolHandler", url).Start()
	case "darwin":
		err = exec.Command("open", url).Start()
	default:
		err = fmt.Errorf("unsupported platform")
	}
	if err != nil {
		log.Fatal(err)
	}

}
