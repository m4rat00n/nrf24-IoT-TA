<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.0/jquery.min.js"></script>
    <script type="text/javascript">
    	var auto_refresh = setInterval(function(){
    		$('#real_monitoring').load('get_data.php').fadeIn('slow');
    	},100);
    </script>
    <style>
        @import url("https://fonts.googleapis.com/css?family=Nunito:700");

*{
    padding: 0;
    margin: 0;
    box-sizing: border-box;
}
html{
    font-size: 10px;
    font-family: 'Nunito', sans-serif;
    scroll-behavior: smooth;
}
a{
    text-decoration: none;
}
.container{
    min-height: 60vh;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: start;
}

.section-title{
    font-size: 4rem;
    font-weight: 300;
    color: black;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: .2rem;
    text-align: center;
}
.section-title span{
    color: brown;
}

/* tab section */
#tab {
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100vw;
    height: auto;
}

#tab .tab{
    min-height: 8vh;
    background-color: rgba(31, 30, 30, 0.24);
    transition: .3s ease background-color;
}
#tab .nav-bar{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: 100%;
    max-width: 1300px;
    padding: 0 10px;
}
#tab .nav-bar h1{
    color: white;
    font-size: 3.5rem;
}

#tab .nav-list ul {
    list-style: none;
    position: absolute;
    background-color: rgb(31, 30, 30);
    width: 100vw;
    height: 100vh;
    left: 100%;
    top: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 1;
    overflow-x: hidden;
    transition: .3s ease left;
}
#tab .nav-list ul.active{
    left: 0;
}

#tab .nav-list ul a{
    font-size: 2.5rem;
    font-weight: 500;
    letter-spacing: .2rem;
    text-decoration: none;
    color: white;
    text-transform: uppercase;
    padding: 20px;
    display: block;
}

#tab .nav-list ul a::after{
    content: attr(data-after);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0);
    color: rgba(240, 240, 255, 0.021);
    font-size: 13rem;
    letter-spacing: 50px;
    z-index: -1;
    transition: .3s ease letter-spacing;
}
#tab .nav-list ul li:hover a::after {
    transform: translate(-50%, -50%) scale(1);
    letter-spacing: initial;
}

#tab .nav-list ul li:hover a{
    color: brown;
}

#tab .hamburger{
    height: 60px;
    width: 60px;
    display: inline-block;
    border: 3px solid white;
    border-radius: 50%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100;
    cursor: pointer;
    transform: scale(.6);
    margin-right: 20px;
}

#tab .hamburger .bar {
    height: 2px;
    width: 30px;
    position: relative;
    background-color: white;
    z-index: -1;
}

#tab .hamburger .bar::after,
#tab .hamburger .bar::before{
    content: '';
    position: absolute;
    height: 100%;
    width: 100%;
    left: 0;
    background-color: white;
    transition: .3 ease;
    transition-property: top, bottom;
}
#tab .hamburger .bar::after{
    top: 8px;
}
#tab .hamburger .bar::before{
    bottom: 8px;
}
#tab .hamburger.active .bar::before{
    bottom: 0;
}
#tab .hamburger.active .bar::after{
    top: 0;
}
/* tab end section */

/* header section */
#header{
    background-size: cover;
    background-position: top center;
    position: relative;
}
#header::after{
    content: '';
    position:absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 100%;
    background-color: black;
    opacity: .7;
    z-index: -1;
}
#header .header{
    max-width: 1500px;
    margin: 0 auto;
    padding: 0 50px;
    justify-content: flex-start;
}
#header h1{
    display: block;
    width: fit-content;
    font-size: 3.7rem;
    position: relative;
    color: transparent;
    animation: text_reveal .5s ease forwards;
    animation-delay: 1.5s;
}
#header h1 span{
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 0;
    background-color: brown;
    animation: text_reveal_box 1s ease;
    animation-delay: 1s;
}
#header .about{
    display: inline-block;
    padding: 10px 30px;
    color: antiquewhite;
    background-color: transparent;
    border: 2px solid antiquewhite;
    font-size: 2rem;
    text-transform: uppercase;
    letter-spacing: .1rem;
    margin-top: 36px;
    transition: .3s ease;
    transition-property: background-color, color;
}
#header .about:hover {
    color: white;
    background-color: brown;
}
/* header end section */

/* about us section */
#aboutus .aboutus{
    background-color: #FBEFD9;
    text-align: center;
    max-width: 100%;
    margin: 0 auto;
    padding: 30px 0;
}

#aboutus .aboutus-top p{
    font-size: 1.5rem;
    margin-top: 5px;
    line-height: 2.5rem;
    font-weight: 300px;
    letter-spacing: .05rem;
    margin-left: 30px;
    margin-right: 30px;
}
/* about us end section */

/* prediction section */
#prediction .prediction {
    background-color: #FFFCF1;
    flex-direction: column;
    max-width: 100%;
    margin: 0 auto;
    padding: 100px 0;
    text-align: center;
}

#prediction .prediction-header p{
    margin-top: 20px;
    margin-bottom: 30px;
    font-size: 1.5rem;
    line-height: 2.5rem;
    font-weight: 300px;
    letter-spacing: .05rem;
    margin-left: 30px;
    margin-right: 30px;
}

#prediction .prediction-bottom {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

#prediction .prediction-item {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    background-color: #FFFCF1;
    width: 350px;
    overflow: hidden;
    border-radius: 10px;
    box-shadow: 0px 0px 18px 0 #0000002c;
}

input {
    border-radius: 10px !important;
    height: 50px !important;
    width: 300px;
    margin-top: 20px;
    margin-bottom: 10px;
    text-align:center;
    font-size: 15px;
}

select{
    border-radius: 10px !important;
    height: 43px !important;
    width: 100%;
}

button {
    border-radius: 20px !important;
    outline: none !important;
    height: 40px !important;
    margin: 20px;
    width: 200px;
    color: whitesmoke !important;
    background: brown !important;
    background: -webkit-linear-gradient(to right, brown, brown) !important; 
    background: linear-gradient(to right, brown, brown) !important; 
}
  
button:hover {
    cursor: pointer;
}
.bottom p{
    color: black !important;
    background: #F8F8FF;
    width: 1145px;
    margin: auto;
    size: 10px;
}
/* prediction end section */

/* data real-time section */

#data .data {
    background-color: #fffae9;
    flex-direction: column;
    max-width: 100%;
    height:100%;
    margin: 0 auto;
    text-align: center;
}

#data .flexbox {
    margin: 20px;
    border-radius: 20%;
    height: 200px;
    width: 100%;
}

#data .section-title{
    margin-top: 30px;
}
.row {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
    display: flex;
    padding: 20px;
}

.row1 {
    background-color: #FFFCF1;
    position: relative;
    flex: 1;
    width: 30%;
    margin: 10px;
    height: 200px;
    border-radius: 5px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}

.row1 h1{
    font-size: 200%;
    margin-top: 25px;
}

.rowa {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
    display: flex;
    padding: 10px;
    padding-left: 20%;
    padding-right: 20%;
}
.row2 {
    background-color: #FFFCF1;
    position: relative;
    flex: 1;
    width: 50%;
    margin: 10px;
    height: 200px;
    border-radius: 5px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}

.row2 h1{
    font-size: 200%;
    margin-top: 25px;
}
.sensor{
    font-size: 400%;
    text-align: center;
    margin-top: 7%;
}

.satuan {
    font-size: 150%;
    text-align: center;
    margin: 2%;
}
/* data real-time end section */

/* keyframes */
@keyframes text_reveal_box{
    50%{
        width: 100%;
        left: 0;
    }
    100% {
        width: 0;
        left: 100%;
    }
}
@keyframes text_reveal{
    100%{
        color: white;
    }
}
/* keyframes end */

/* media query for Desktop */
@media only screen and (min-width: 1200px){
    #tab .hamburger{
        display: none;
    }
    #tab .nav-list ul{
        position: initial;
        display: block;
        height: auto;
        width: fit-content;
        background-color: transparent;
    }
    #tab .nav-list ul li{
        display: inline-block;
    }
    #tab .nav-list ul li a{
        font-size: 1.5rem;
    }
    #tab .nav-list ul a:after {
        display: none;
    }
}
    </style>

    <title>Stasiun Cuaca Lokal</title>
    <link rel="icon" type="image/x-icon" href="images/favicon.jpg">
</head>
<body>
    <!--tab section-->
    <section id="tab">
        <div class="tab container">
            <div class="nav-bar">
                <div class="brand">
                    <a href="#header"><h1>Welcome</h1></a>
                </div>
                <div class="nav-list">
                    <div class="hamburger"><div class="bar"></div></div>
                    <ul>
                        <li><a href="#header" data-after="Home">Home</a></li>
                        <li><a href="#aboutus" data-after="Tentang Kami">Tentang Kami</a></li>
                        <li><a href="#data" data-after="Data Real-Time">Data Real-Time</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
    <!--tab end section-->

    <!--header section-->
    <section id="header">
        <div class="header container">
            <div>
                <h1>Stasiun Cuaca Lokal,<span></span></h1>
                <h1>Jawa Barat<span></span></h1>
                <a href="#aboutus" type="button" class="about">Tentang Kami</a>
            </div>
        </div>
    </section>
    <!--header end section-->

    <!--about section-->
    <section id="aboutus">
        <div class="aboutus container">
            <div class="aboutus-top">
                <h1 class="section-title">Tentang <span>Kami</span></h1>
                <p>Sistem cuaca kami menghasilkan dan menyediakan pemantauan cuaca untuk wilayah Bandung terutama perkebunan yang disesuaikan dengan kebutuhan penelitian dan pengguna dalam
                meningkatkan pengawasan dan prediksi terhadap perubahan cuaca. Laporan cuaca disajikan secara Realtime dengan pengambilan data dengan sensor yang sudah dikalibrasi untuk mendapatkan nilai yang akurat.
                Tujuan kami adalah untuk menyajikan pengawasan cuaca di suatu wilayah dengan akurat dan dapat dimanfaatkan untuk kepentingan suatu pihak yang membutuhkan.</p>
            </div>
        </div>
    </section>
    <!--about end section-->

    <!--data real-time section-->
    <div id="real_monitoring"></div>
    <!--data real-time end section-->
    <script src="{{url_for('static',filename='js/app.js')}}"></script>
</body>
</html>
