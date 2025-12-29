import { useContext } from "react"
import { context } from "./Store"

export default function A(){
    const {incHandler} = useContext(context)
    return(

        <div>
            <h1>Z</h1>
            <button onClick={incHandler}>+</button>
        </div>
    )
}