// var UserGist = React.createClass({
//   getInitialState: function() {
//     return {
//       username: '',
//       lastGistUrl: ''
//     };
//   },

//   componentDidMount: function() {
//     $.get(this.props.source, function(result) {
//       var lastGist = result[0];
//       if (this.isMounted()) {
//         this.setState({
//           username: lastGist.owner.login,
//           lastGistUrl: lastGist.html_url
//         });
//       }
//     }.bind(this));
//   },

//   render: function() {
//     return (
//       <div>
//         {this.state.username}'s last gist is
//         <a href={this.state.lastGistUrl}>here</a>.
//       </div>
//     );
//   }
// });

// ReactDOM.render(
//   <UserGist source="https://api.github.com/users/octocat/gists" />,
//   mountNode
// );


var data = [ 0,1,2,3 ]
var data = [
    {
        title: 'New Shaaaaver!',
        entities: [ 'Philips', 'John Doe', 'PSV'],
        sitename: 'deal.eindhoven.nl'
    }
]

var News = React.createClass({
    render: function(){
        var data = this.props.data;
        return ( <div>
            <h2>{data.title}</h2>
            <i>{data.sitename}</i>
            <div>{data.entities.join(', ')}</div>
        </div> )
    }
});

var Basket = React.createClass({
    render: function() {
        console.log(this.props.data);
        return (
            <div>
          {
              this.props.data.map(function(d) {
                return <News data={d}></News>
              })
          }</div>
        );
  }
});

ReactDOM.render(
  <div><Basket data={data}/></div>,
  document.getElementById('example')
);

// TODO:
// 1. News Element
// 2. Query it from elastic
