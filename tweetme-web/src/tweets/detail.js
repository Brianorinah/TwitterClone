import React, { useState } from "react";
import { ActionBtn } from "./buttons";

export function ParentTweet(props) {
  const { tweet } = props;

  return tweet.parent ? (
    <div className="row">
      <div className="col-11 p-3 mx-auto border rounded">
        <p className="mb-0 text-muted small">Retweet</p>
        <Tweet hideActions className={""} tweet={tweet.parent} />
      </div>
    </div>
  ) : null;
}

export function Tweet(props) {
  const { tweet, didRetweet, hideActions } = props;
  const [actionTweet, setActionTweet] = useState(
    props.tweet ? props.tweet : null
  );
  // const className = props.className
  //   ? props.className
  //   : "col-10 mx-auto col-md-6";

  const path = window.location.pathname;
  const match = path.match(/(?<tweetid>\d+)/);
  const urlTweetId = match ? match.groups.tweetid : -1;
  const isDetail = `${tweet.id}` === `${urlTweetId}`;

  if (match) {
  }
  const handleLink = (event) => {
    event.preventDefault();
    window.location.href = `/${tweet.id}`;
  };

  const handlePerformAction = (newActionTweet, status) => {
    if (status === 200) {
      setActionTweet(newActionTweet);
    } else if (status === 201) {
      if (didRetweet) {
        didRetweet(newActionTweet);
      }
    }
  };
  return (    
    <div>
      <div>
        <p>
          {tweet.id}-{tweet.content}
        </p>
        <ParentTweet tweet={tweet} />
      </div>
      <div className="btn btn-group">
        {actionTweet && hideActions !== true && (
          <React.Fragment>
            <ActionBtn
              tweet={actionTweet}
              didPerformAction={handlePerformAction}
              action={{ type: "like", display: "Likes" }}
            />
            <ActionBtn
              tweet={actionTweet}
              didPerformAction={handlePerformAction}
              action={{ type: "unLike", display: "UnLike" }}
            />
            <ActionBtn
              tweet={actionTweet}
              didPerformAction={handlePerformAction}
              action={{ type: "retweet", display: "Retweet" }}
            />
          </React.Fragment>
        )}
        {isDetail === true ? null : (
          <button className="btn btn-outline-primary btn-sm" onClick={handleLink}>
            View
          </button>
        )}
      </div>
    </div>
  );
}
