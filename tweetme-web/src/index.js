import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import { TweetsComponent ,TweetDetailComponent} from "./tweets";
import * as serviceWorker from "./serviceWorker";

const appEl = document.getElementById("root");
if (appEl) {
  ReactDOM.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
    appEl
  );
}

const e = React.createElement;
const tweetsEl = document.getElementById("tweetme");
if (tweetsEl) {
  ReactDOM.render(e(TweetsComponent, tweetsEl.dataset), tweetsEl);
}

const tweetDetailElements = document.querySelectorAll(".tweetme-detail")
tweetDetailElements.forEach(container =>{
  ReactDOM.render(e(TweetDetailComponent, container.dataset), container)
})

serviceWorker.unregister();
