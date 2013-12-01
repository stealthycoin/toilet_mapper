/**
  - Example usage
     tapi({
       noun: "toilet"
       ,verb: "create"
       ,data: { name: "Pooper" }
       ,callback: function(data){ 
          console.log("I'm called when the we have the response to our request.")
       }
     });

   - Also can automatically deal with form submission for you:
     HTML: 
       <form id='add_pooper_form'>
           <input name='name' />
           <input type='submit' name='Submit' />
       </form>
     JS: 
       tapi_auto_form('add_pooper_form', 
          {  noun: "toilet"
           , verb: "create"
           , callback : function(data){ console.log("Automatically submitted"); }
          });

      Then when you submit the form, it will automatically call 
      the python middletier and perform whatever action you’ve
      specified.  
   
   - Note that tapi returns the "jqXHR object" in case you need to use it
     (http://api.jquery.com/jQuery.ajax/#jqXHR):
   
     var jqxhr = tapi({ noun: "toilet", verb: "create", data: {name: "pooper"}});
     jqxhr.done(function(data){ 
       console.log("I'm called when we have the response to our request."); 
     });
     
   - tapi_auto_form takes an optional argument which is a function to 
     manipulate a jqXHR object:
     
     function jfun(jqXHR){
       j.done(function(data){
         console.log("It worked!");
       });
       j.fail(function(data){
         console.log("It failed!");
       });
     }
     tapi_auto_form('add_pooper_form', {noun: "toilet", verb: "create"}, jfun);


**/
function simple_post(url, data, stringify) {
    if (stringify !== undefined) {
        for (o in stringify) {
            if (data[stringify[o]] === undefined) data[stringify[o]] = {}
            data[stringify[o]] = JSON.stringify(data[stringify[o]]);
        }

    }
    return $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: 'json'
    });
}

function simple_handler(url, stringify) {
    return function (data) {
        return simple_post(url, data, stringify);
    }
}

var internal_mapping = {
    "toilet": {
        "retrieve"         : simple_handler("/api/Toilet/get/", ["filters"]),
        "create"           : simple_handler("/api/toilet/create/")
    },
    "review": {
        "retrieve"         : simple_handler("/api/Review/get/", ["filters"]),
        "create"           : simple_handler("/api/review/create/"),
        "upvote"           : simple_handler("/api/review/upvote/"),
        "downvote"         : simple_handler("/api/review/downvote/")
    },
    "user": {
        "login"            : simple_handler("/api/user/login/"),
        "logout"           : simple_handler("/api/user/logout/"),
        "create"           : simple_handler("/api/user/create/"),
        "edit"           : simple_handler("/api/user/edit/")
    },
    "flag": {
        "retrieve_rankings": simple_handler("/api/FlagRanking/get/", ["filters"]),
        "retrieve_flags"   : simple_handler("/api/Flag/get/", ["filters"]),
        "upvote"           : simple_handler("/api/flag/upvote/"),
        "downvote"         : simple_handler("/api/flag/downvote/")
    }
}


    function tapi_error(e) {
        throw ("tAPI error: " + e);
    }

    function server_error(responseText, errorThrown) {
        alert("Server error: " + errorThrown);
    }

    function tapi(params, callback) {
        if (!params.noun) {
            tapi_error("Request made with no noun.");
        }

        if (!params.verb) {
            tapi_error("Request made with no verb.");
        }

        if (!internal_mapping.hasOwnProperty(params.noun)) {
            tapi_error("Noun " + params.noun + " is not recognized");
        }

        if (!internal_mapping[params.noun].hasOwnProperty(params.verb)) {
            tapi_error("Noun " + params.noun + " does not have the verb " + params.verb);
        }

        if (params.data === undefined) {
            params.data = {};
        }
        var jqxhr = internal_mapping[params.noun][params.verb](params.data);
        if (params.callback !== undefined) {
            jqxhr.done(params.callback);
        }

        jqxhr.fail(function (e, z, errorThrown) {
            if (errorThrown === "UNAUTHORIZED") {
                var err = JSON.parse(e.responseText);
                window.location = "/signin?error=" + encodeURI(err.error);
            } else {
                server_error(e.responseText, errorThrown);
            }
        });

        return jqxhr;
    }

    function tapi_auto_form(form_id, tapi_params, jqxhr_f) {
        $(document).ready(function () {
            $('#' + form_id).submit(function (e) {
                $('#' + form_id + " button").attr('disabled', true);
                e.preventDefault();

                if ($('#' + form_id).data('submit_in_process') === true) return;
                $('#' + form_id).data('submit_in_process', true);
                if ($('#' + form_id).attr('data-validate') === "parsley" && !$('#' + form_id).parsley('isValid')) {
                    $('#' + form_id + " button").attr('disabled', false);
                    $('#' + form_id).data('submit_in_process', false);
                    return;
                }

                tapi_params.data = {};
                $('#' + form_id + ' [name]').each(function () {
                    tapi_params.data[$(this).attr('name')] = $(this).val();
                });

                var t = tapi(tapi_params);
                t.done(function () {
                    $('#' + form_id).data('submit_in_process', false);
                    $('#' + form_id + " button").attr('disabled', false);
                });
                if (jqxhr_f !== undefined) jqxhr_f(t);
            });
        });
    }
