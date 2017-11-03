var app = angular.module('lineAnimation', []);

		app.controller('myCtrl', ['$scope', '$document', '$window', function($scope, $document, $window) {


        var svgContainer = d3.select(document.getElementById("canvas")).append("svg")
                            .attr("width", 200)
                            .attr("height", 1000);
 

    	DrawLine = function (x1, y1, x2, y2, r) {
					//Draw the line
			 var line = svgContainer.append("line")
			                          .attr("x1", x1)
			                          .attr("y1", y1)
			                         .attr("x2", x1)
			                         .attr("y2", y1)
			                         .attr("stroke-width", r)
			                         .attr("stroke", "black")
			                         .transition()
			                         .delay(300)
			                         .duration(2000)
			                         .attr("x2", x2)
			                         .attr("y2", y2);
				}                             
					
			CreatePoint = function(x, y, r) {
				var circle = svgContainer.append("circle")
								.attr("cx", x)
								.attr("cy", y)
								.attr("r", 0);

				circle.transition()
						.duration(1500)   //measured in Mili Seconds
						.delay(200)
						.attr("r", r);
			}

            GetElementAbsoluteTop= function(eleId) {
                var element = document.getElementById(eleId);
                var elementTop = element.getBoundingClientRect().top;
                var absoluteTop = elementTop + window.pageYOffset;

                return absoluteTop;
            }
			
            var absolutePositionExp = GetElementAbsoluteTop('experience-col')
			var absolutePosition1 = GetElementAbsoluteTop('Northrop-Header');
            var absolutePosition2 = GetElementAbsoluteTop('X-Country-Header');
            var positionOffset1 = absolutePosition1 - absolutePositionExp;
            var positionOffset2 = absolutePosition2 - absolutePositionExp;

			//Perform on load as well
			$document.on('scroll', function() {
			    //update path
			    //var textDiv1Position = textDiv1.getBoundingClientRect().top;
				//var textDiv2Position = textDiv2.getBoundingClientRect().top;

                var topPadding = 20;
                var horizontalPosition = 50;
                var point1 = positionOffset1 + topPadding;
                var point2 = positionOffset2 + topPadding;

			    if(window.pageYOffset > absolutePosition1 )
			    {
                    CreatePoint(horizontalPosition, point1, 30);
                    
			    	//this.CreatePoint(50, 50, 30);
                    DrawLine(horizontalPosition, point1, horizontalPosition, point2, 10);
                    
                    CreatePoint(horizontalPosition, point2, 30);
			    }
			    
			    if(0 > absolutePosition2 ) {
			    	//CreatePoint(50, 300, 50, 400, 10);

			    }

			});
		}]);