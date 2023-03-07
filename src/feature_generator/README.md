# cpp-project-template

> A general C++ project template, using a Makefile with building, running and testing capabilities.

It includes:

* a Makefile with build and run rules, with GDB and config flags already present.
* a project structure
* `.vscode` folder with the necessary config files to use VSCode code correction and the integrated GDB debugger.

### VSCode extentions

If you use `VSCode`:

* `ms-vscode.cpptools`: extention comming with GDB debugger integration.

### C++ compiler

`sudo apt install clang` 

## Getting Started

### Use the Github template

First, click the green `Use this template` button near the top of this page. This will take you to Github's [Generate Repository](https://github.com/cpp-best-practices/cpp_boilerplate_project/generate) page. Fill in a repository name and short description, and click `Create repository from template`. This will allow you to create a new repository in your Github account,
prepopulated with the contents of this project. Now you can clone the project locally and get to work!

```
git clone https://github.com/<user>/<your_new_repo>.git
```

1. Inside the cloned repo folder, make the necessary directories for compilation with `make dirs`. Then build and start coding/debugging.
2. Compile `main` with `make build`.
3. Compile `test` with `make built_test`.
4. Run `main` with `make run`.
5. Run `test` with `make run_test`.
