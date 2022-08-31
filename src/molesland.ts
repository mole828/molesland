import Logger from "https://deno.land/x/logger@v1.0.2/logger.ts";

class Func {
  constructor(
    readonly func: (request: Request) => Response = () =>
      new Response(JSON.stringify({ message: "NOT FOUND" }), {
        status: 404,
        headers: {
          "content-type": "application/json; charset=utf-8",
        },
      })
  ) {}
}

export class Router extends Func {
  logger = new Logger();
  map = new Map<string, Router>();
  __rout(paths: string[], request: Request):Response {
    this.logger.info(paths);
    if (paths.length) {
      const path = paths.shift();
      if (path) {
        this.logger.info(paths, path);
        const next = this.map.get(path);
        if (next) {
          return next.__rout(paths, request);
        }
        throw 404;
      }
      return this.func(request)
    }
    return this.func(request)
  }
}

function pathMaker (url:string) {
  const paths = url.split("/");
  paths.shift(); // 'http:'
  paths.shift(); // ''
  paths.shift(); // `localhost:${port}`
  return paths;
}

export class Server extends Router {
  async listen({ port }: { port: number } = { port: 8080 }) {
    this.logger.info(`molesland listen: http://localhost:${port}/`);
    const listener = Deno.listen({ port });
    for await (const conn of listener) {
      const httpConn = Deno.serveHttp(conn);
      for await (const requestEvent of httpConn) {
        const { request } = requestEvent;
        request.headers
        const { url, headers:x } = request;
        this.logger.info(url, x);
        const paths = pathMaker(url);
        try {
          const response = this.__rout(paths, requestEvent.request);
          requestEvent.respondWith(response);
        } catch (e) {
          if (e.constructor === Number) {
            this.logger.info(e);
            if(e===404){
              requestEvent.respondWith(new Func().func(request));
            }
          } else {
            this.logger.error(e);
            requestEvent.respondWith(new Response('unkown error',{
              status: 400,
            }));
          }
        }
      }
    }
  }
}
