//binarySearch for the index of cmpVal. If cmpVal isn't in A then 
//   we return the index of the closest element
// if def === 1 then it will return the closest greater element
// if def === -1 it will return the closest smaller element
function binarySearch(A, cmpVal, def, valfn, i, j){
    if(!A.length) return -1; 
    var valfn = valfn || function(x){ return x; }
    var def = def || 0;
    if(i === undefined){ i = 0; }
    if(j === undefined){ j = A.length; }
    if(i >= j) {
	if(def === -1){
	    if(i > 0) return i - 1;
	    else return i;
	}
	else if(def === 0){
	    var v0 = 999999999;
	    var v2 = 999999999;
	    if(i > 0) v0 = valfn(A[i-1])
	    if(i + 1 < A.length) v2 = valfn(A[i+1]);
	    var a = [Math.abs(v0 - cmpVal)
		     ,Math.abs(valfn(A[i]) - cmpVal)
		     ,Math.abs(v2 - cmpVal)]
	    var closest = a.indexOf(Math.min.apply(Math, a));
	    if(closest === 0) return i - 1; 
	    else if(closest === 2){ return i + 1; }
	    else return i; 
	}
	else if(def === 1){
	    if(i + 1 < A.length) return i + 1;
	    else return i; 
	}
	else { throw "Parameter 'def' must be -1, 0, or 1"; }
    }

    var idx = i + Math.floor((j - i)/2);
    if (idx < 0 || idx + 1 > A.length){ throw "Bad idx: "+idx+" not in [0, "+A.length+"]"; }
    var v = valfn(A[idx]);

    if(v > cmpVal){ return binarySearch(A, cmpVal, def, valfn, i, idx); }
    if(v === cmpVal){ return idx; }
    if(v < cmpVal){ return binarySearch(A, cmpVal, def, valfn, idx+1, j); }
}

bsScrollLoad = function(){
    var containerID = undefined;
    var bsScrollLoading = false;
    var lastLoad = 0;
    var lastHeightRecondense = 0;
    var recondensing = false;
    
    //These variables will be set inside init
    var cb;
    var ct; 
    var queryCallback;
    var numToLoad;
    var queryFn;
    var attemptLoad;

    function init(containerID_, templateID
			      , queryFn_, numToLoad_, settings){
	if(bsScrollLoading) return;
	bsScrollLoading = true; 

	containerID = containerID_;
	numToLoad = numToLoad_ || 20;
	queryFn = queryFn_;

	var t = Handlebars.compile($(templateID).html());
	var c = $(containerID);
	var numLoaded = 0;
	var loadedItems = [];

	c.html('');
	c.before("<div class='condenserTop'></div>");
	c.after("<div class='condenserBottom'></div>");
	cb = c.next('.condenserBottom');
	ct = c.prev('.condenserTop');

	queryCallback = function (items){
	    c = $(containerID);
	    for(var i = 0; i < items.length; i++){
		var idx = numLoaded + i;
		//var item = $(t(items[i])).appendTo(c).attr('data-loadedItemsIdx', idx);
		//var top = item.offset().top;
		
		//, bottom: top + item.outerHeight(true) 
		c.next('.loading').slideUp().remove();
		loadedItems[idx] = { item: items[i]
				     , top: undefined
				     , bottom: undefined
				     , visible: false
				   }
		c.append(t(items[i]));
	    }

	    
	    bsScrollLoading = false;
	    numLoaded += items.length;
	    //recondense();
	}


	function recondense(diff){
	    console.log("Attempt to recondense: "+recondensing);
	    if(!loadedItems.length) { recondensing = false; return; }
	    if(recondensing){  return; }
	    recondensing = true;

	    var hideProximity = $(window).height() * 2.2; //pixels
	    var wst = $(window).scrollTop(); 
	    var visibleWindowTop = wst - hideProximity;
	    var visibleWindowBottom = wst + $(window).height() + hideProximity;
	    
	    var visibleMinIdx = binarySearch(loadedItems, visibleWindowTop,
					     -1, function(x){ return x.bottom; }) || 0;
	    var visibleMaxIdx = binarySearch(loadedItems, visibleWindowBottom,
					     1, function(x){ return x.top; }) || loadedItems.length - 1;
	    var children = $(c).children();
	    for(var i = 0; i < children.length; i++){
		var ci = $(children[i]);
		var cii = ci.attr('data-loadedItemsIdx');
		if(loadedItems[i] === undefined){
		    console.log(loadedItems);
		    throw "loadedItems["+i+"] is undefined.";
		}
	    }

	    //Defaults
	    var lowerIdx = 0;
	    var uppderIdx = loadedItems.length - 1; 

	    if(children.length){
		var idx = $(children[0]).attr('data-loadedItemsIdx');
		//Readjust the top spacer
		// our previous adjustments were just for continuity
		// this one will be entirely correct.
		var top = loadedItems[idx].top;
		ct.css('height', top - ct.offset().top + "px");
		var lowerIdx = $(children[0]).attr('data-loadedItemsIdx');
		var upperIdx = $(children[children.length - 1]).attr('data-loadedItemsIdx');
	    }


	    console.log("VisibleMinIdx: "+visibleMinIdx);
	    console.log("VisibleMaxIdx: "+visibleMaxIdx);
	    for(var i = visibleMinIdx; i < visibleMaxIdx; i++){

		if(loadedItems[i] === undefined){
		    console.log(loadedItems);
		    throw "loadedItems["+i+"] is undefined "; 
		}
		if(loadedItems[i].visible === true){  continue;}
		loadedItems[i].visible = true;
		if(i < lowerIdx){
		    var item = $(t(loadedItems[i].item)).prependTo(c);
		    item.attr('data-loadedItemsIdx', i);
		    ct.css('height'
			   , (ct.height() - (loadedItems[i].bottom - loadedItems[i].top)
			     ) +'px');
		}
		else {
		    var item = $(t(loadedItems[i].item)).appendTo(c).attr('data-loadedItemsIdx', i);

		    console.log("ITEM: ", item, item.length);
		    console.log(loadedItems[i].item);
		    if(loadedItems[i].top === undefined){
			loadedItems[i].top = item.offset().top;
			loadedItems[i].bottom = loadedItems[i].top + item.outerHeight(true);
			item.attr('data-loadedItemsIdx', i);

/*			$('body').append(
			    "<div style='position: absolute; left: 0px; top: "
				+loadedItems[i].top+"px; background-color: white;'>"+i+"</div>");*/
		    }

		    cb.css('height'
			   , (cb.height() - (loadedItems[i].bottom - loadedItems[i].top)
			     ) +'px')
		}
	    }
	    bsScrollLoading = false;
	    recondensing = false; 
	}



	if(settings === undefined){ settings = {} }

	var wh = $(window).height(); 
	var loadDistance = settings.loadDistance || wh * 1.5; 
	var loadIncrement = settings.loadIncrement || 20;
	var delay = settings.delay || 2000;

	var condenseInterval = 100; //pixels


	//Initial
	//queryFn(queryCallback, 0, numToLoad);
	
	var lastEnd = -1; 
	function _attemptLoad(){
	    var end = numLoaded + numToLoad;
	    if(end == lastEnd) return; //no more to load


	    var t  = new Date().getTime();
	    var st = $(window).scrollTop();
	    var diff = st - lastHeightRecondense;

	    if( Math.abs(diff) > condenseInterval){
		lastHeightRecondense = st; 
		//recondense(diff);
	    }
	    if((st + loadDistance >= $(document).height()
		&& t - delay > lastLoad)
	       || st + $(window).height() + 50 >= $(document).height())
	
	    {
		var z = c.children();
		var lastChildIdx =  $(z[ z.length - 1]).attr('data-loadedItemsIdx');
		if(lastChildIdx !== z.length - 1){
		    recondense();
		}
		var z = c.children();
		var lastChildIdx =  $(z[ z.length - 1]).attr('data-loadedItemsIdx');
		lastLoad = t;

		/*c.find(".loading").remove();
		c.after("<div class='loading'>Loading</div>").hide().fadeIn();*/
		lastEnd = end;
		queryFn(queryCallback, numLoaded, end);
	    }
	    else {  }
	}
	attemptLoad = _attemptLoad;
	$(document).ready(function(){ attemptLoad() });
	$(window).scroll(attemptLoad);
    }

    function reset(){
	$(containerID).html('');
	loadedItems = [];
	lastLoad = 0;
	lastHeightRecondense = 0;
	ct.css('height', '0');
	cb.css('height', '0');
	queryFn(queryCallback, 0, 20);
    }

    function changeQueryFn(newFn){
	queryFn = newFn;
    }
    
    function changeNumToLoad(n){ numToLoad = n; }

    return { init: init 
	     , reset: reset
	     , changeQueryFn: changeQueryFn
	     , changeNumToLoad: changeNumToLoad
	     , attemptLoad: attemptLoad
	   }
}
