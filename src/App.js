import React, { useState, useEffect } from "react";
import "./scss/style.scss";
var md5 = require('md5');

function App() {

  const [nameInput, setNameInput] = useState("");
  const [emailInput, setEmailInput] = useState("");
  const [commentInput, setCommentInput] = useState("");
  const [comments, setComments] = useState([]);
  const [timer, setTimer] = useState(0);
  const [formError, setFormError] = useState("");
  const [sortParameter, setSortParameter] = useState("email");
  useEffect(() => {
    const interval = setInterval(() => {
        getComments();
    }, timer);
    setTimer(1000);
    return () => clearInterval(interval);
  }, [comments]);


  function getComments() {
    fetch("/getComments?sortby=" + sortParameter)
      .then((res) => res.json())
      .then((data) => {
        let html = "";
        data.forEach(function (userComment) {
          html += "<div>";
          html += "<img src='http://www.gravatar.com/avatar/" + md5(userComment['email']) + "' />";
          html +=   "<div>";
          html +=     "<p>" + userComment['inserted_on'] + "</p>";
          html +=     "<p>By <a href=mailto:'" + userComment['email'] + "'>" + userComment['name'] + "</a></p>";
          html +=   "</div>";
          html +=   "<p>" + userComment['comment'] + "</p>";
          html += "</div>";
        });
        setComments(<div className="commentsHistory" dangerouslySetInnerHTML={{ __html: html }} />);
      }, []);
  }

  function handleSort(e) {
    setSortParameter(e.target.dataset.sort);
    getComments();
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    setFormError("");

    if (!nameInput || !emailInput || !commentInput) {
      setFormError(<p className="error" dangerouslySetInnerHTML={{ __html: "All fields of the form must be completed to submit a comment." }} />);
      return;
    }

    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({'name':nameInput, 'email':emailInput, 'comment':commentInput})
    };

    fetch("/saveComment", requestOptions)
      .then((res) => res.json())
      .then((data) => {
      }).catch(function() {
        setFormError(<p className="error" dangerouslySetInnerHTML={{ __html: "Make sure all the fields on the form are valid." }} />);
    });
  }

  return (
    <div>
      <div className="filtersModule">
        <span data-sort="date" onClick={handleSort}>Sort by Date</span>
        <span data-sort="name" onClick={handleSort}>Sort by Name</span>
        <span data-sort="email" onClick={handleSort}>Sort by Email</span>
      </div>
      <div className="commentsModule">
        <p className="title">Comments</p>
        {comments}
        <p className="title">Leave a Comment</p>
        {formError}
        <form onSubmit={handleSubmit}>
          <label>Your name *</label>
          <input type="text" placeholder="Phil Leggeter" name="name" value={nameInput} onChange={e => setNameInput(e.target.value)}/>
          <label>Your email *</label>
          <input type="text" name="email" placeholder="philleggeter@gmail.com" value={emailInput} onChange={e => setEmailInput(e.target.value)}/>
          <label>Comments</label>
          <textarea type="text" name="comment" value={commentInput} onChange={e => setCommentInput(e.target.value)}></textarea>
          <button type="submit">Submit comment</button>
        </form>
      </div>
    </div>
  );
}

export default App;
