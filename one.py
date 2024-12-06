def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    file_path = '/path/to/your/document.txt'
    content = read_file(file_path)
    print(content)

if __name__ == "__main__":
    main()