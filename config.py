import json

try:
    with open("config.json") as f:
        conf = json.loads(f.read())
        env = conf.get("environment", "development")
        cache_path = conf.get("cache_path", "/var/www/html/cache-files")
except Exception as e:
    print(str(e))
    env = "development"
    cache_path = "/var/www/html/cached-files"

if __name__ == "__main__":
    print(env)
    print(cache_path)


