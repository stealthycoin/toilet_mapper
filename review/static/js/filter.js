/** REMOVE THIS AFTER TESTING **/
var filter_map = ["faggot"];

String.prototype.repeat = function(num){
  return new Array(num + 1).join(this);
}

function filter_content(string_content) {
    
    for(var i=0; i<filter_map.length; ++i){

        // create a regular expression to use when finding inappropriate words
        var pattern = new RegExp('\\b' + filter_map[i] + '\\b', 'g');

        // create a new string filled with '*'
        var replacement = '*'.repeat(filter_map[i].length);

       string_content = string_content.replace(pattern, replacement);
   }

  // string_content now has filtered content instead of inappropriate word
  return string_content;

}
/********************************/
