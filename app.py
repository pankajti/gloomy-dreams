from gloomy_dreams.dash_main import app

if __name__ == "__main__":
    app.index_string = """
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>Gloomy Dreams</title>
            {%favicon%}
            {%css%}

            <!-- Matomo Tracking Code -->
            <script type="text/javascript">
              var _paq = window._paq = window._paq || [];
              /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
              _paq.push(['trackPageView']);
              _paq.push(['enableLinkTracking']);
              (function() {
                var u="https://mindcurd4.matomo.cloud/";
                _paq.push(['setTrackerUrl', u+'matomo.php']);
                _paq.push(['setSiteId', '1']);
                var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
                g.async=true; g.src='https://cdn.matomo.cloud/mindcurd4.matomo.cloud/matomo.js'; s.parentNode.insertBefore(g,s);
              })();

              // ➡️ Custom function to track Analyze button clicks
              function trackAnalyzeClick() {
                _paq.push(['trackEvent', 'Button', 'Click', 'Analyze Button']);
              }
            </script>
            <!-- End Matomo Tracking Code -->

        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    """

    app.run(debug=True,host='0.0.0.0', port=8050)