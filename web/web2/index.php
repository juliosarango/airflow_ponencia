<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sitio Web 2</title>
    <style>
        body {
            background-color: #d9f2d9;
        }

        h2 {
            color: blue;
        }

        p {
            color: red;
        }
    </style>
</head>

<body>

    <h2>Listado de archivos respaldados - Web2</h2>
    <?php
    $thefolder = "./files_web2/";
    $listadoArchivos = "";
    $existeArchivos = 0;
    if ($handler = opendir($thefolder)) {
        $listadoArchivos = "<ul>";
        while (false !== ($file = readdir($handler))) {
            if ($file !== "." && $file !== "..") {
                $filePath = $thefolder . $file;
                $listadoArchivos .= "<li><a href='$filePath' target='_blank'>$file</a></li>";
                $existeArchivos++;
            }
        }
        $listadoArchivos .=  "</ul>";
        closedir($handler);
    }
    if ($existeArchivos == 0) {
        $listadoArchivos = "No hay archivos subidos";
    }

    echo $listadoArchivos;
    ?>

</body>

</html>