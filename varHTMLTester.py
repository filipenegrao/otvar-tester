from pagebot.fonttoolbox.objects.font import Font
from webbrowser import open_new_tab
from os import getcwd, system
import datetime

FONTPATH = './variable_ttf/DecovarAlpha-VF.ttf'  # the link for your variable font

font = Font(FONTPATH, lazy=False)

# --------------------------- html stuff ---------------------------

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>%(fontFamilyName)s</title>
    <style>
    @font-face {
    font-family: "%(fontFirstName)s";
    src: url(%(fontPath)s);
    }

    html {
        background-color: black;
    }

    body {
        padding: 100px;
    }

    h1, h2, h3 {
        font: small sans-serif;
        color: #C0C0C0;
    }

    h3 {
        padding: 80px 0 0 0;
        margin-bottom: 0;
    }

    h1, h3 {
        font-weight: bold;
    }

    h2 {
        border-bottom: 3px solid #C0C0C0;
        padding-bottom: 15px;
    }

    p {
        z-index: 0;
        position: relative;
        margin: 0px;
        padding: 5px;
        padding-top: 0.2em;
        line-height: 1em;
        font: 100px "%(fontFirstName)s";
        font-feature-settings: "kern" on, "liga" on, "calt" on;
        -moz-font-feature-settings: "kern" on, "liga" on, "calt" on;
        -webkit-font-feature-settings: "kern" on, "liga" on, "calt" on; 
        -ms-font-feature-settings: "kern" on, "liga" on, "calt" on;
        -o-font-feature-settings: "kern" on, "liga" on, "calt" on;
        font-variation-settings: "wght" 97;
    }

    .labeldiv {
        width: 100%%;
        display: inline-block;
        padding-top: 40px;
    }

    label {
        z-index: 2;
        position: absolute;
        pointer-events: none;
        width: 100%%;
        height: 2em;
        margin: 0;
        padding: 0;
        font: small sans-serif;
        color: #C0C0C0;
        padding-top: 20px;
    }

    .slider {
        z-index: 1;
        position: relative;
        -webkit-appearance: none;
        -moz-appearance: none;
        appearance: none;
        width: 100%%;
        height: 3px;
        border-radius: 5px;   
        background: #C0C0C0;
        padding: 0px;
        margin: 0px;
    }

    .slider::-webkit-slider-thumb {
        z-index: 3;
        position: relative;
        -webkit-appearance: none;
        -moz-appearance: none;
        appearance: none;
        width: 15px;
        height: 15px;
        border-radius: 10px; 
        background: #C0C0C0;
        cursor: auto;
    }

    a {
        color: #808080;
    }

    #form {
        z-index: 100;
        float: right;
        width: 20%%;
        padding-top: 0px;
        background-color: black;
    }

    #textinputwrapper {
        padding-top: 50px;
        width: 75%%;
    }

    #textInput {
        color: #C0C0C0;
        height: 2em;
        background-color: #404040;   
        background: #404040;
        width: 99.4%%;
    }

    #text {
        z-index: -10;
        background-color: white;
        height: 400px;
        padding: 0;
        margin: 0;
        width: 100%%;
    }

    footer p {
        padding-top: 60px;
        font: small sans-serif;
        color: #C0C0C0;
    }
    </style>

    <script>

    function updateParagraph() {
    // update paragraph text based on user input:
    var userinput = document.getElementById("textInput");
    var paragraph = document.getElementById("text");
    paragraph.textContent = userinput.value;
    }
            
    function updateSlider() {
    var body = document.getElementById("text");
    var sliders = document.getElementsByClassName("slider")
    var bodystyle = "";
    var settingtext = "";

    for (var i = 0; i < sliders.length; i++) {
        var sliderID = sliders[i].id;
        var sliderValue = sliders[i].value;
        var label = document.getElementById("label_"+sliderID);
        label.textContent = ""+sliderID+": "+sliderValue

        if (sliderID == "fontsize") {
            // Text Size Slider
            bodystyle += "font-size: "+sliderValue+"px;"
            label.textContent += "px"

        } else if (sliderID == "lineheight") {
            // Line Height Slider
            bodystyle += "line-height: "+sliderValue/100.0+"em;"
            label.textContent += "%%"
        
        } else {
            // OTVar Slider
            if (settingtext != "") { settingtext += ", " }
            settingtext += '"' + sliderID + '" ' + sliderValue
        }
    }

        bodystyle += "font-variation-settings: "+settingtext+";"
        body.setAttribute("style", bodystyle);
    }
    </script>
</head>

<body onload="updateSlider();">
    <h1>Variable Tester</h1>
    <h2>Font: %(fontFamilyName)s | Output: %(currentTime)s</h2>

    <div id="form">
        <div class="labeldiv"><label class="sliderlabel" id="label_fontsize">fontsize</label><input type="range" min="10" max="200" value="100" class="slider" id="fontsize" oninput="updateSlider();"></div>
        <div class="labeldiv"><label class="sliderlabel" id="label_lineheight">lineheight</label><input type="range" min="100" max="240" value="120" class="slider" id="lineheight" oninput="updateSlider();"></div>
        
        <!-- VAR DIVS ADDED -->
        <h3>Variable Axis</h3>
%(axisDivs)s

    </div>
    
    <div id="textinputwrapper">
    <input type="text" value="Type here..." id="textInput" onkeyup="updateParagraph();" onclick="this.select();" />
    <p id="text">hamburgfontvs</p>
    </div>

<footer>
<p>Compatible with the latest version of <a href="https://www.apple.com/safari/" target="_blank">Safari</a> and <a href="https://www.google.com/chrome/"target="_blank">Chrome</a>.</p>
</footer>

</body>

</html>
"""


HTML_DIV = '''
        <div class='labeldiv'>
        <label class='sliderlabel' id='label_%s'>%s</label>
        <input type='range' min='%s' max='%s' value='%s' class='slider' id='%s' oninput='updateSlider();'>
        </div>
'''


# --------------------------- wrappers ---------------------------

def divAxisBuilder(variableFont):
    u"""
    from pagebot.fonttoolbox.objects.font import Font
    fontPath = '/path/to/your/font.ttf'
    font = Font(fontPath, install=False, lazy=False)

    Get a variable font, check all axis available inside this font.
    Then, this function adds this data to a div, in order to build a html
    file that has a slider for each axis.

    Returns all divs that are necessary to build the html latter.
    """

    listDivAxis = []

    for key in variableFont.axes.keys():
        div_axis_str = (key, key, variableFont.axes[key][0], variableFont.axes[key][2], variableFont.axes[key][1], key)
        listDivAxis.append(HTML_DIV % div_axis_str)

    axisDiv2add = "\n".join(listDivAxis)
    return axisDiv2add


def htmlWraper(variableFont, url, divs):
    fontFamilyName = variableFont.info.familyName
    fontFirstName = fontFamilyName.split()
    fontFirstName = fontFirstName[0]

    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    filenameHTML = ''.join((fontFamilyName.lower()).split()) + ".html"

    filePath = "./" + filenameHTML
    
    # Write HTML
    f = open(filePath,'w+')
    d = dict(fontFamilyName=fontFamilyName, fontFirstName=fontFirstName, fontPath=FONTPATH, currentTime=now, axisDivs=divs)
    htmltxt = HTML % d
    f.write(htmltxt)
    f.close()

    # terminalInstruction = 'cd "%s"; open .' % filePath
    bashCommand = 'cd "%s"; open ./%s' % (getcwd(), filenameHTML)
    system(bashCommand)

    # open_new_tab(filePath)
    print "File saved to %s" % FONTPATH


# -------------------------------------------------------------

divs = divAxisBuilder(font)  # divs to add to the html file
urlpath = "./%s" % (font.info.familyName)  # where the font will be saved

htmlWraper(variableFont=font, url=urlpath, divs=divs)

