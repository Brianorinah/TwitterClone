import React, { useState } from "react";
import { TweetsList } from "./list";
import {TweetCreate} from './create'


export function TweetsComponent(props) {
  //Receives username props from index.html data-username attribute

  const canTweet = props.canTweet === "false" ? false : true;
  const [newTweets, setNewTweets] = useState([]);
  const handleNewTweet = (newTweet) => {
    //backend api response handler
    let temptNewTweets = [...newTweets];
    temptNewTweets.unshift(newTweet);
    setNewTweets(temptNewTweets);
  };
  return (
    <div className={props.className}>
      {canTweet === true && (
        <TweetCreate didTweet={handleNewTweet} className="col-12 mb-3" />
      )}
      <TweetsList newTweets={newTweets} {...props} />
    </div>
  );
}
