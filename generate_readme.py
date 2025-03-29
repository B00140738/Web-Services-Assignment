from main import app


def generate_readme():
    with open("README.txt", "w") as f:
        f.write("API Endpoints:\n\n")
        for route in app.routes:
            # Skip the docs route to avoid listing it
            if route.name == "Swagger UI":
                continue
            # Correctly accessing the 'methods' attribute for HTTP methods
            f.write(f"{', '.join(route.methods)} {route.path}\n")

        f.write("\nFor more detailed documentation, please visit: ")
        f.write("http://127.0.0.1:8000/docs\n")


if __name__ == "__main__":
    generate_readme()
    print("README.txt generated successfully")

