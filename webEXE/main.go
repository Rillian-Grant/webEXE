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

//go:embed logo.txt
var logo string

var PORT string = "8080"

func main() {
	print(logo)

	r := http.NewServeMux()

	embeddedFiles, err := fs.Sub(embeddedFiles, "www")
	if err != nil {
		exit(err)
	}
	r.Handle("/", http.FileServer(http.FS(embeddedFiles)))

	log.Println("Starting server on port " + PORT)
	l, err := net.Listen("tcp", "localhost:"+PORT)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Opening browser")
	openBrowser("http://localhost:" + PORT)

	log.Println("Server started. Press Ctrl+C to exit")
	err = http.Serve(l, r)
	if err != nil {
		exit(err)
	}
}

func exit(err error) {
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("\nPress any key to exit")
	fmt.Scanln()
	panic(err)
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
		exit(err)
	}

}
