import pandas as pd
import numpy as np
import plotly.express as px
from plotly.offline import plot
import os
import re

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    # import information
    data = "data.csv"
    df = pd.read_csv(data)

    # get columns of interest
    id = "ID"
    di = "Difficulty"
    wl = "Workload"
    rt = "Rating"
    rv = "Reviews"
    cs = "ComboScore"
    lr = "LogReviews"
    dp = "Department"
    lk = "URL"

    # exclude outliers and courses with minimal reviews
    df = df[df[wl] < 40.0]
    df = df[df[rt] > 2.0]
    df = df[df[rv] >= 5]

    # prepare color scaling and sizing
    dfn = df[[di,wl,rt]]
    dfn = (dfn - dfn.mean()) / (dfn.max() - dfn.min())
    df[cs] = dfn[rt] - dfn[di] - dfn[wl]
    df[lr] = np.sqrt(df[rv])

    # prepare urls for opening later
    df[lk] = "https://omscentral.com/course/"+df[id]
    
    # some urls prepend numbers with 'O' if preceded with a 2nd dash
    links = []
    for string in df[lk]:
        contents = string.split("-")
        if len(contents) > 2:
            new_content = ["O"+i for i in contents[2:]]
            contents[2:] = new_content
        links.append('-'.join(contents))
    df[lk] = links

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # set up figure
    fig = px.scatter_3d(
        df,
        x=di,
        y=wl,
        z=rt,
        color=cs,
        title=f"OMSCentral Course {di} vs. {wl} vs. {rt}",
        size=lr,
        size_max=50,
        symbol=dp,
        labels={
            di:di+" (x/5)",
            wl:wl+" (hr/wk)",
            rt:rt+" (x/5)",
            cs:cs+f" = {rt}-{wl}-{di} (normalized)"
        },
        hover_name=id,
        hover_data={
            cs:False,
            lr:False,
            rv:True,
            dp:False,
            lk:False
            },
        custom_data=[lk]
        )
    
    fig.update_layout(hovermode="x", legend_orientation="h")
    fname = os.path.basename(__file__.rstrip(".py")+".html")
    # fig.write_html(fname)
    #fig.show()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Adding functionality to open links by editing html/js of generated fig
    # https://community.plotly.com/t/hyperlink-to-markers-on-map/17858/4
    
    # Get HTML representation of plotly.js and this figure
    plot_div = plot(fig, output_type='div', include_plotlyjs=True)

    # Get id of html div element that looks like
    # <div id="301d22ab-bfba-4621-8f5d-dc4fd855bb33" ... >
    res = re.search('<div id="([^"]*)"', plot_div)
    div_id = res.groups()[0]

    # Build JavaScript callback for handling clicks
    # and opening the URL in the trace's customdata 
    js_callback = """
    <script>
    var plot_element = document.getElementById("{div_id}");
    plot_element.on('plotly_click', function(data){{
        console.log(data);
        var point = data.points[0];
        if (point) {{
            console.log(point.customdata[0]);
            window.open(point.customdata[0]);
        }}
    }})
    </script>
    """.format(div_id=div_id)

    # Build HTML string
    html_str = """
    <html lang="en">
    <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width"/>
    </head>
    <body>
    {plot_div}
    {js_callback}
    </body>
    </html>
    """.format(plot_div=plot_div, js_callback=js_callback)

    # Write out HTML file
    with open(fname, 'w') as f:
        f.write(html_str)