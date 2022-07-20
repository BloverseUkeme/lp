function myFunc() {
  return OAUTH_ENV 
}

$('#twitter-button').on('click', function() {
  // Initialize with your OAuth.io app public key

  OAUTH_ENV = myFunc()
  OAuth.initialize(OAUTH_ENV);
  // Use popup for OAuth
  OAuth.popup('twitter').then(twitter => {
    // Retrieves user data from oauth provider
    // console.log(twitter.me());

    twitter.me().done(function(data) {
    // do something with `data`, e.g. print data.name

    // console.log(data.alias)

    
        $.ajax({
            url:"/handle_reg",
            type:"POST",
            contentType: "application/json",
            data: JSON.stringify(data.alias)});
    
})
});
})
