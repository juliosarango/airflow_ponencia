<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sitio Web 1</title>
    <style>
        body {
            background-color: powderblue;
        }

        h1,
        h2 {
            color: blue;
        }

        hr {
            width: 800px;
            margin-top: 50px;
            margin-left: 0;
        }
    </style>
</head>

<body>
    <?php
    session_start();
    if (isset($_SESSION['message']) && $_SESSION['message']) {
        printf('<b>%s</b>', $_SESSION['message']);
        unset($_SESSION['message']);
    }
    ?>

    <h3>Subida de archivos servidor web1</h3>
    <form method="POST" action="upload.php" enctype="multipart/form-data">
        <div>
            <span>Upload a File:</span>
            <input type="file" name="uploadedFile" />
        </div>
        <input type="submit" name="uploadBtn" value="Upload File" />
    </form>

    <hr>

    <h2>Listado de archivos subidos</h2>
    <?php
    $thefolder = "./files_web1/";
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