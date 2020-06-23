class HeadlinesView extends React.Component {
    constructor(props) {
        super(props)
        this.search_term = new URLSearchParams(window.location.search).get("q");
        this.state = {result: "", pass_avg: 0, act_avg: 0, sent_avg: 0, rows: []}
    }

    componentDidMount() {
        console.log("calling with search term"+this.search_term)
        fetch("http://localhost:5000/analyze/search?q="+this.search_term)
        .then(response => response.json())
        .then(data => this.setState({
            result: JSON.stringify(data),
            pass_avg: data['stats']["nnsubj:pass"]["mean"],
            act_avg: data['stats']["nnsubj"]["mean"],
            sent_avg: data['stats']["nsentiment"]["mean"],
            rows: data['data']
        }));
    }

    render() {
        if(!this.search_term) {
          return  (<div>{"No search term - need ?q=seearch_term"}</div>)
        }
        if(!this.state.result) {
            return (<div>
                {"Loading..."}
                <img src={"loading.gif"}  />

            </div>)
        }
        let r = this.state.rows.map((row, index)=> {
            if(row["nnsubj:pass"] > 0) {return (
            <div>
                <h3 style={{color:'red'}}>{row["original_text"]+ " (Passive)"}</h3>
                <p>{"Sentiment: "+ row["sentiment"]}</p>
                <p>{"Mentions: "+ JSON.stringify(row["mentions"])}</p>
                <p>{"Passive voice: "+JSON.stringify(row["nsubj:pass"])}</p>
                <p>{"Active voice: "+JSON.stringify(row["nsubj"])}</p>
            </div>
            )}
            else {return (
            <div>
            <h3 style={{color:'blue'}}>{row["original_text"]+ " (Active)"}</h3>
            <p>{"Sentiment: "+ row["sentiment"]}</p>
            <p>{"Mentions: "+ JSON.stringify(row["mentions"])}</p>
            <p>{"Passive voice: "+JSON.stringify(row["nsubj:pass"])}</p>
            <p>{"Active voice: "+JSON.stringify(row["nsubj"])}</p>
            </div>
         )}
        }
        )
        return (<div>
            <h1>{"Passive Voice avg: "+this.state.pass_avg}</h1>
            <h1>{"Activate Voice avg: "+this.state.act_avg}</h1>
            <h1>{"Sentiment avg: "+this.state.sent_avg}</h1>
            {r}
            {this.state.result}
            </div>)
    }
}