GetElementSize = function(eleId) {
    var element = document.getElementById(eleId);
    var elementHeight = element.getBoundingClientRect().height;
    return elementHeight;
}

// Draw point1, connect it with a line, then draw point2
DrawConnectionBar = function(point1, point2, line) {
    var duration = 1000;
    var totalDuration = 0;
        
    DrawLine(point1, point2, line.r, totalDuration);

    totalDuration += duration;

    CreatePoint(point2, totalDuration);
}

//Get the top position of the element specified
GetElementAbsoluteTop= function(eleId) {
    var element = document.getElementById(eleId);
    var elementTop = element.getBoundingClientRect().top;
    var absoluteTop = elementTop + window.pageYOffset;

    return absoluteTop;
}

GetElementAbsoluteBottom= function(eleId) {
    var element = document.getElementById(eleId);
    var elementBottom = element.getBoundingClientRect().bottom;
    var absoluteBottom = elementBottom + window.pageYOffset;

    return absoluteBottom;
}

//Get the difference in position between two elements.
// <Remarks>Top starts at 0, so bottom element position is a greater number </remarks>
GetPositionDelta = function(elementTop, elementBottom) {
    var absolutePositionTop = GetElementAbsoluteTop(elementTop);
    var absolutePositionBottom = GetElementAbsoluteTop(elementBottom);
    var seperationFromElements = absolutePositionBottom - absolutePositionTop;
    return seperationFromElements;
}

function LineObj(point1, point2, r) {
    this.point1 = point1;
    this.point2 = point2;
    this.r = r;
}

function PointObj(x, y, r) {
    this.x = x;
    this.y = y;
    this.r = r;
}

function ElementData(elementId, elementsParentId) {
    this.id = elementId;
    this.parentId = elementsParentId;
    this.absolutePosition = GetElementAbsoluteTop(elementId);
    this.positionFromParentDiv = GetPositionDelta(elementsParentId, elementId);
    this.absolutePositionBottom = GetElementAbsoluteBottom(elementId);

    var elementPaddingFromTop = 20;
    this.positionForPoint = this.positionFromParentDiv + elementPaddingFromTop;
    
    // Determines if the line is animated
    this.segmentAnimated = false;
}

AnimatePointToPoint = function(horizontalPosition, y1, y2, r, lineThickness) {
    var point1 = new PointObj(horizontalPosition, y1, r);
    var point2 = new PointObj(horizontalPosition, y2, r);
    var line = new LineObj(point1, point2, lineThickness);
    DrawConnectionBar(point1, point2, line);
}

// Gets the dimensions of all element datas
GetElementData = function() {
    var elementIds = ['experience-col', 'Northrop-Header', 'X-Country-Header',
    'isdr-header', 'internship-header'];

    var elementObjs = [];
    // add all cols that need to be animated to the element obj array
    for(i=1; i<elementIds.length; i++){
        var elementName = elementIds[i];
        var newElement = new ElementData(elementName, 'experience-col');
        elementObjs.push(newElement);
    }

    return elementObjs;
}

var svgContainer;


// Builds the SVG container for the line elements to be kept in
BuildSvgContainer = function() {
    var experienceRowHeight = GetElementSize('experience-col');
    var svgContainer = d3.select(document.getElementById("canvas")).append("svg")
                        .attr("width", 200)
                        .attr("height", experienceRowHeight);
    return svgContainer;
}

ScreenResize = function() {
    // clear containers lines
    d3.select(document.getElementById("canvas")).html("");

    //TODO: Implement Screen resize function
    // //Rebuild SVG conatiner to the new dimensions of the exp col
    // svgContainer = BuildSvgContainer();

    // //RepopulateAnimations(elementObjs);

    // //rebuild the element objs
    // elementObjs = GetElementData();

}

var app = angular.module('lineAnimation', []);

app.controller('myCtrl', ['$scope', '$document', '$window', function($scope, $document, $window) {
    var elementObjs = GetElementData();
    
    window.addEventListener('resize', ScreenResize );    
    
    svgContainer = BuildSvgContainer();
    

    DrawLine = function (point1, point2, r, delay) {
        //Draw the line
        //start at position 1 then move to position 2
        var line = svgContainer.append("line")
                            .attr("x1", point1.x)
                            .attr("y1", point1.y)
                                .attr("x2", point1.x)
                                .attr("y2", point1.y)
                                .attr("stroke-width", r)
                                .attr("stroke", "black")
                                .transition()
                                .delay(delay)
                                .duration(1000)
                                .attr("x2", point2.x)
                                .attr("y2", point2.y);
    }                             
                
    CreatePoint = function(point, delay) {
        var circle = svgContainer.append("circle")
                        .attr("cx", point.x)
                        .attr("cy", point.y)
                        .attr("r", 0);

        circle.transition()
                .delay(delay)
                .duration(1000)   //measured in Mili Seconds
                .attr("r", point.r);
    }
            
    // Padding for animation from top of parent element
    var topPadding = 20; //TODO: make this half the height of the anchor ele
    var horizontalPosition = 50; // TODO: probably should be half the width of the col

    var absolutePositionExp = GetElementAbsoluteTop('experience-col')    
    
    //bool represents if experience point is animated
    var experiencePointAnimated = false;
    
    $document.on('scroll', function() {
        var pointRadius = 20;
        var lineThickness = 10;

        // Y offset plust a padding to animate before the target is reached
        var yOffsetPadding = window.pageYOffset + 300;

        //TODO: group with other section objects
        if(!experiencePointAnimated && yOffsetPadding > absolutePositionExp)
        {
            //draw start point
            var firstElement = elementObjs[0];
            var point1 = new PointObj(horizontalPosition, 
                firstElement.positionForPoint, pointRadius);                    
            CreatePoint(point1, 0);
            experiencePointAnimated = true;
        }

        for(i=0; i<elementObjs.length; i++){
            var curEle = elementObjs[i];
            
            if( !curEle.segmentAnimated  
                && yOffsetPadding > curEle.absolutePosition ){
                
                // If not on last ele
                if( i != elementObjs.length - 1){
                    // Animate line
                    var nextEle = elementObjs[i+1];

                    AnimatePointToPoint(horizontalPosition, curEle.positionForPoint, 
                        nextEle.positionForPoint, pointRadius, lineThickness);
                    curEle.segmentAnimated = true;
                } else {
                    AnimatePointToPoint(horizontalPosition, curEle.positionForPoint, 
                        curEle.absolutePositionBottom, pointRadius, lineThickness);
                    curEle.segmentAnimated = true;
                }
                
            }

        }
    });
}]);