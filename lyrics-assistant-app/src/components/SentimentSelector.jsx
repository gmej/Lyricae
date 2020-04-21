import React from 'react'
import * as sentiments from './sentiments.json' 

export default class SentimentSelector extends React.Component {

    constructor(props) {
        super(props);
        this.state = {value: sentiments.happy};
        this.handleChange = this.handleChange.bind(this);
      }

      componentDidMount(){
          this.props.selectSentiment(this.state.value)
      }
    
      handleChange(event) {
        this.setState({value: event.target.value});
        this.props.selectSentiment(event.target.value)
      }
    
      render() {
        let text = "Your sentiment to write about: "
        return (
          <form>
            <label>
            {text}
              <select value={this.state.value} onChange={this.handleChange}>
                <option value={sentiments.happy}>{sentiments.happy}</option>
                <option value={sentiments.angry}>{sentiments.angry}</option>
                <option value={sentiments.relaxed}>{sentiments.relaxed}</option>
                <option value={sentiments.sad}>{sentiments.sad}</option>
              </select>
            </label>
            <input type="submit" value="Submit" />
          </form>
        );
      }
}