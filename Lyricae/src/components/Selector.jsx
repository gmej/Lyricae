import React from 'react'

export default class Selector extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            min: this.props.min || 3,
            max: this.props.max || 15,
            value: this.props.initial || 7
        }
        this.handleChange = this.handleChange.bind(this);
        this.getValues = this.getValues.bind(this);
      }

    componentDidMount(){
        this.props.selectNumber(this.state.value)
    }

    handleChange(event) {
        this.setState({value: event.target.value});
        this.props.selectNumber(event.target.value)
    }
    
    getValues(){
        let lista= []
        for(let i=this.state.min; i<=this.state.max; i++){
            lista.push(<option key={"option_"+i}>{i}</option>)
        }
        return lista
    }
    
    render() {
    return (
        <form>
        <label>
            <select value={this.state.value} onChange={this.handleChange}>
                {this.getValues()}
            </select>
        </label>
        </form>
    );
    }
}