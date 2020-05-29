import React, { useEffect, useState } from "react";
import { TweetsList } from "./list";
import { TweetCreate } from "./create";
import { apiTweetDetail } from "./lookup";
import { Tweet } from "./detail";

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

export function TweetDetailComponent(props) { 

  const { tweetId } = props;
  const [lookup, setDidLookup] = useState(false);
  const [tweet, setTweet] = useState(null);

  const handlebackendLookUp = (response, status) => {
    if (status === 200) {
      setTweet(response);
    } else {
      alert("There was an error finding your tweet.");
    }
  };
  useEffect(() => {
    if (lookup === false) {
      apiTweetDetail(tweetId, handlebackendLookUp);

      setDidLookup(true);
    }
  }, [tweetId, lookup, setDidLookup]);

  return tweet === null ? null : (
    <Tweet tweet={tweet} className={props.className} />
  );
}
