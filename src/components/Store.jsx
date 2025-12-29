import { createContext, useState } from "react";
const context = createContext();


export default function Store(props){
const [count ,setcount] = useState(0);

function incHandler(){
    setcount(count+1);
}
    return(
     <context.Provider value={{count,incHandler}}>
        {props.children}
     </context.Provider>
    )
}

export { context };
