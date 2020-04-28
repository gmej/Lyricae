import React from 'react';

export default class CloudItem extends React.Component {

    constructor(props){
        super(props)

        this.onClick = this.onClick.bind(this)
    }

    onClicK(w){
        this.props.onClicK(w)
    }

    render(){
        return(
            <div className="tag-item-wrapper"
                onClick={this.onClicK(this.props.text)}>
            <div>
            { this.props.text }
                </div>
            </div>
    )}


}