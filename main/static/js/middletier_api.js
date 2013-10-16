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

function simple_post(url, data){
    return $.ajax({ url: url, type: 'POST', data: data, dataType: 'json'});
}

function simple_handler(url){
    return function(data){ return simple_post(url, data); }
}

var internal_mapping = {
    "toilet": {
        "retrieve": function (){}
        ,"create": simple_handler("/api/toilet/create/")
    }
    ,"review": {
        "retrieve": simple_handler("/api/review/retrieve/")
        ,"create": simple_handler("/api/review/create/")
        ,"vote": function (){}
    }
    ,"user": {
        "retrieve": function(data){}
        ,"create": function(){}
        ,"vote": function(){}
    }
}


function tapi_error(e){ throw ("tAPI error: " + e); }

function tapi(params){
    if(!params.noun){ tapi_error("Request made with no noun."); }
    if(!params.verb){ tapi_error("Request made with no verb."); }
    if(!internal_mapping.hasOwnProperty(params.noun)){
        tapi_error("Noun "+params.noun+" is not recognized"); 
    }

    if(!internal_mapping[params.noun].hasOwnProperty(params.verb)){
        tapi_error("Noun "+params.noun+" does not have the verb "+params.verb);
    }

    
    if(params.data === undefined){ params.data = {}; }
    var jqxhr = internal_mapping[params.noun][params.verb](params.data); 
    if(params.callback !== undefined){ jqxhr.done(params.callback); }
    
    return jqxhr;
}

function tapi_auto_form(form_id, tapi_params, jqxhr_f){
    $(document).ready(function(){
        $('#'+form_id).submit(function(e){
            e.preventDefault();
            if($('#'+form_id).attr('data-validate') === "parsley"
               && !$('#'+form_id).parsley('isValid')) return;
            
            tapi_params.data = {};
            $('#'+form_id+' [name]').each(function(){
                tapi_params.data[$(this).attr('name')] = $(this).val();
            });

            var t = tapi(tapi_params);
            if(jqxhr_f !== undefined) jqxhr_f(t);
        });
    });
}
