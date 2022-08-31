import { Router, Server } from "./src/molesland.ts";

(()=>{
  const server = new Server(()=>{
    return new Response("hello");
  });
  server.map.set('hello', new Router((request)=>{
    console.log(request.body)
    return new Response('world')
  }))
  server.listen();
})()
