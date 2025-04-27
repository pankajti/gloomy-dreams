from gloomy_dreams.dash_main import app

if __name__ == "__main__":
    app.index_string = app.index_string = """
<!DOCTYPE html>
<html lang="en">
<head>
    {%metas%}
    <title>Financial News Sentiment Analyzer - Gloomy Dreams AI Tool</title>
    {%favicon%}
    {%css%}
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="Analyze financial news sentiment using AI agents. Summarizes stock market news and classifies sentiment into positive, negative, or neutral using multi-LLM workflows. Built with Dash, LangChain, Together.ai, and OpenAI.">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="Gloomy Dreams - Financial News Sentiment Analyzer" />
    <meta property="og:description" content="Summarize and analyze financial news sentiment across stock tickers using AI agents and LLMs. Built with Dash, LangChain, and Together.ai." />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://gloomy-dreams.onrender.com/" />
    
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

      // Custom Event Tracker for Analyze Button
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