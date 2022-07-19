<?php
include "connect.php";
$query = "SELECT * FROM monitoring WHERE id = 1";
$result = mysqli_query($connect, $query);
while($row = mysqli_fetch_array($result)){
    echo '<section id="data">';
        echo '<div class="data container">';
            echo '<div class="data-header">';
                echo '<h1 class="section-title">Data <span>Real-Time</span></h1>';
            echo '</div>';
        echo '<div class="flexbox">';
            echo '<div class="row">';
                echo '<div class="row1">';
                    echo '<h1>Kecepatan Angin</h1>';
                    echo '<p class="sensor">' . $row['kec_angin'] . '</p>';
                    echo '<p class="satuan">km/s</p>';
                echo '</div>';
                echo '<div class="row1">';
                    echo '<h1>Curah Hujan</h1>';
                    echo '<p class="sensor">' . $row['curah_hujan'] . '</p>';
                    echo '<p class="satuan">mm</p>';
                echo '</div>';
                echo '<div class="row1">';
                    echo '<h1>Kelembaban Tanah</h1>';
                    echo '<p class="sensor">' . $row['soil_mois'] . '</p>';
                    echo '<p class="satuan">%</p>';
                echo '</div>';
            echo '</div>';
            echo '<div class="rowa">';
                echo '<div class="row2">';
                    echo '<h1>Temperature</h1>';
                    echo '<p class="sensor">' . $row['temp'] . '</p>';
                    echo '<p class="satuan">celcius</p>';
                echo '</div>';
                echo '<div class="row2">';
                    echo '<h1>Humidity</h1>';
                    echo '<p class="sensor">' . $row['humidity'] . '</p>';
                    echo '<p class="satuan">%</p>';
                echo '</div>';
            echo '</div>';
        echo '</div>';
        echo '</div>';
    echo ' </section>';
}
?>
