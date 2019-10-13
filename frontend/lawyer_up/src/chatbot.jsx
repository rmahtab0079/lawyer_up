
import React, { Component } from 'react';

// export class Chatbot extends Component {
//     render() {
//        return (
//           <div >
//                 <h1>Lawyer Up</h1>
//           </div>

//        )
//     }
// }



import ChatBot from 'react-simple-chatbot';
 
const steps = [
  {
    id: '0',
    message: 'Welcome to react chatbot!',
    trigger: '1',
  },
  {
    id: '1',
    message: 'Bye!',
    end: true,
  },
];
 
// ReactDOM.render(
//   <div>
//     <ChatBot steps={steps} />
//   </div>,
//   document.getElementById('root')
// );
//<ChatBot steps={steps} />

export class Chat extends Component {
    render() {
       return (
          <div >
                <h1>Lawyer Up</h1>
                 
                <iframe
    allow="microphone;"
    width="1000"
    height="430"
    src="https://console.dialogflow.com/api-client/demo/embedded/c9e8f1a4-ae82-44d9-a2a4-10ac7ef086a2">
</iframe>
        </div>

       )
    }
}