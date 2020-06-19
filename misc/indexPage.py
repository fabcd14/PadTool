
# coding: utf-8

import cgi 
import os.path, time

html = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="generator" content="Jekyll v3.8.5">
    <title>PadTool Monitoring</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
    <script>   
        $(document).ready(function() {
            function updateDiv(){
                $.ajax({
                    url: "slide/dls",
                    dataType: "json",
                    cache: false,
                    success: function(data) {
                        $('#dls').html("");
                        $('#dls').html(`
                            <h6 class="border-bottom border-gray pb-2 mb-0">DLS</h6>
                            
                            `);
                        $.each( data, function( key, val ) {
                            $('#dls').append(`
                                <div class="media text-muted pt-3"></div>
                                    <p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
                                        <span id="dls">
                                            <strong class="d-block text-gray-dark">`+key+`</strong>
                                            `+val+`
                                        </span>
                                    </p>
                                </div>
                            `);
                            
                            
                        });
                    }             
                });

                $.ajax({
                    url: "slide/sls",
                    dataType: "json",
                    cache: false,
                    success: function(data) {
                        $('#sls').html("");
                        $.each( data, function( key, val ) {
                            $('#sls').append(`
                                <div class="col-md-4">
                                    <div class="card mb-4 shadow-sm">
                                        <img src="`+"slide/" + val + `?_=`+ Date.now() + `" style="margin: auto; width: 320px; height: 240px; text-align: center;"/>
                                        <div class="card-body">
                                            <p class="card-text"></p>
                                            <h5 class="card-title">`+val+`</h5>
                                            <div class="d-flex justify-content-between align-items-center">
                                                <div class="btn-group">
                                                    <a href="`+"slide/" + val + `?_=`+ Date.now() + `"><button type="button" class="btn btn-sm btn-outline-secondary">View</button></a>
                                                </div>
                                                <small class="text-muted"></small>
                                            </div>
                                        </div>
                                    </div>
                                </div>`
                            );
                        });
                    }             
                });              
            }
            updateDiv();
            setInterval(updateDiv, 5000);
        });
    </script>


    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }
    </style>
    <!-- Custom styles for this template -->
    <!--<link href="album.py" rel="stylesheet">-->
  </head>
  <body>
    <header>
  <div class="navbar navbar-dark bg-dark shadow-sm">
    <div class="container d-flex justify-content-between">
      <a href="#" class="navbar-brand d-flex align-items-center">
        <strong>PadTool</strong>
      </a>
    </div>
  </div>
</header>

<main role="main">

  <section class="jumbotron">
    <div class="container">
      <h1 class="jumbotron-heading">$radioName</h1>
      <p class="lead text-muted">$slogan</p>
      <p>
        <!--<a href="#" class="btn btn-primary my-2">Main call to action</a>
        <a href="#" class="btn btn-secondary my-2">Secondary action</a>-->
      </p>
    </div>
  </section>

  <div class="album py-5 bg-light">
    <div class="container">  
        <div id="dls" class="my-3 p-3 bg-white rounded shadow-sm">
            
        </div>
      <div id="sls" class="row">
        
        
      </div>
    </div>
  </div>

</main>

<footer class="text-muted">
  <div class="container">
    <p class="float-right">
      <a href="#">Back to top</a>
    </p>
  </div>
</footer>
<!--<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
      <script>window.jQuery || document.write('<script src="/docs/4.3/assets/js/vendor/jquery-slim.min.js"><\/script>')</script><script src="https://getbootstrap.com/docs/4.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-xrRywqdh3PHs8keKZN+8zzc5TX0GRTLCcmivcbNJWm2rs5C8PRhcEn3czEjhAO9o" crossorigin="anonymous"></script>--></body>
</html>

"""
def generate():
    return html