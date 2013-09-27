<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Bezirkswahlen</title>
  
  <!--[if lt IE 9]>
    <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
  <![endif]-->

  <script src="http://ajax.googleapis.com/ajax/libs/webfont/1/webfont.js" type="text/javascript" async=""></script>
  <link rel="stylesheet" href="css/style.css" type="text/css">
  </style>
</head>
<body>
  <?php 
    $search_string = $_GET['s'];
  ?>
  <div id="wrapper">
    <header>
    	<div class="inside">
      	<h1>Regionalbezirkssuche</h1>
      </div>
    </header>
    <div id="menu-placeholder"></div>
    <section class="inside" id="content">
      <article id="search">
        <form action="<?php echo $PHP_SELF;?>" method="get">
          <p>Straßenname: <input name="s" size="40" <?php if ($search_string == '') { echo "placeholder=\"Name der Straße\""; } else { echo "value=\"" . $search_string . "\""; } ?>> <input type="submit"></p>
        </form>
      </article>
    	<h2>Suche nach Straße:</h2>
    	<h3><?php echo $search_string; ?> </h3>
      <?php 
        /* Config */
        $datei = file_get_contents("data/strassenverzeichnis_hh.xml");

        /* Work */
        $xml = simplexml_load_string( $datei );

        foreach ( $xml->record as $data ) {
          if ($data->Straße == $search_string) {
            echo "<article>";
              echo "<p><strong>Straße</strong>: " . $data->Straße . "</p>";
              echo "<p><strong>Hausnummer</strong>: " . $data->HausNR . "</p>";
              echo "<p><strong>Stadtteil</strong>: " . $data->Stadtteil . "</p>";
              echo "<p><strong>Ortsteil ID</strong>: " . $data->Ortsteil . "</p>";
              echo "<p><strong>PLZ</strong>: " . $data->PLZ . "</p>";
              echo "<p><strong>Wahlkreis Nummer</strong>: " . $data->Wahlkreis_Nr . "</p>";
              echo "<p><strong>Wahlkreis Name</strong>: " . $data->Wahlkreis_Name . "</p>";
            echo "</article>";
          }
        }
      ?>
    </section>
    <footer>
    	<div class="inside">
      	<p>Hier ein Piratigen cc Footer denken</p>
      </div>
    </footer>
  </div>   
</body>
</html>