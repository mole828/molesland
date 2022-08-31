import Logger from "https://deno.land/x/logger@v1.0.2/logger.ts";

export class Server {
  logger = new Logger();
  async listen({ port }: { port: number } = { port: 8080 }) {
    this.logger.info(`molesland listen: http://localhost:${port}/`);
    const listener = Deno.listen({ port })
    for await (const conn of listener) {
      const httpConn = Deno.serveHttp(conn);
      for await (const request of httpConn) {
        request.respondWith(new Response('here is molesland'));
      }
    }
  }
}
