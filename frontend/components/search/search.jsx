import React from 'react';
import Spinner from 'react-bootstrap/Spinner';
import styles from './search.module.css'
import { InputGroup, FormControl } from 'react-bootstrap';
import { Sources } from '../sources/sources';
import { Examples } from '../examples/examples';

export class Search extends React.Component {

    constructor(props) {
        // let a = { time: 2070, link: "https://www.youtube.com/watch?v=AUU9RlDrSo0&t=2070", name: "El Método Rebord #50 - Alberto Fernández", text: "Alejandro Dolina ha dicho: Pero también le digo que no espero nada tampoco, no espero ninguna alegría que provenga de así. Tendría derecho entonces a esperar que ninguna tristeza saliera de su lugar. Y eso es capaz de ser más difícil. Lo que quiero decir es que yo no he estado en mucho de nuestro foro, soy amigo de algunos tipos, generalmente por casualidad, y todo el mundo sabe que soy peronista, pido permiso y nada más. Pero ella parecía una frase que se me atribuye, que se pantosa. ¿Cuál? Dice muchas, pero ésta es especialmente insidiosa porque dice dejemos de pedir perdón, dejemos, somos nosotros los peronistas, ¿no? Dejemos de pedir perdón cuando uno de nosotros comete un delito, un delito. Durísima la frase. Pero eso no es nada con la que sigue. Ellos no tienen a ninguna persona honesta. punto. Alejandro Dorni. Me suena. Yo Tomás Rebord ha dicho: una vez creo que...  Alejandro Dolina ha dicho: Yo no me veo a mí pensando eso, pero ni aunque tuviera razón. " };
        // let b = { time: 2180, link: "https://www.youtube.com/watch?v=AUU9RlDrSo0&t=2180", name: "El Método Rebord #50 - Alberto Fernández", text: "Tomás Rebord ha dicho: Y bueno, a uno de los tienen que ser convencidos primero, digamos. Yo me acuerdo... Ay, era buenísima. Obviamente la voy a atribuir y va a ser difícil de desmentir, pero me acuerdo dos cosas. Siempre me acuerdo cuando una vez te preguntaron por Borges. gorilas y los hay, ¿no? Los ilustres gorilas y te preguntaban pero cómo puedes disfrutar de Borges siendo peronista y te voy a citar mal, pero dijiste pose peronista pero no boludo digamos, creo que lo dijiste mucho más elegante, creo que... ¡Habe dicho estúpido! Y la otra que fue fascinante, porque hace así discusiones yo pasé por etapas más así de sobre intelectualizar las cosas y creo que estoy casi seguro que te lo escuché decir en algún lado que vos dijiste mi se peronista porque quería mantener mis ideales pero quería comprarme un auto. Quería disfrutar" }
        // let answer = "Alejandro Dolina dijo que el fútbol y la política no tienen nada que ver.Explicó que son partes diferentes del cerebro las que se ocupan de cada uno.También dijo que la mayoría del pueblo argentino no mira con simpatía una política de inclusión.Finalmente, mencionó que los jugadores de fútbol están indignados por los impuestos que les cobran por sus ganancias."
        super(props);
        // this.state = { answer: answer, sources: [a, b], answerWords: answer.split(" "), sourcesWords: [], loading: false };
        this.state = { answer: "", sources: [], answerWords: [], sourcesWords: [], loading: false };
    }

    handleSubmit = async (event) => {
        this.setState({ answer: "", sources: "", answerWords: [], sourcesWords: [], loading: true });
        if (event !== undefined) {
            event.preventDefault();
        }
        console.log("searching for topic: " + this.state.value)
        let response = await fetch("api/search?query=" + this.state.value);

        try {
            var result = await response.json();
            if (result.response === undefined) {
                result.answer = "Error in the call";
            }

            this.setState({ answer: result.response.answer });
            this.setState({ answerWords: result.response.answer.split(" ") });
            this.setState({ sources: result.response.sources });
            this.setState({ loading: false })
        }
        catch (err) {
            console.log(err)
            this.setState({ answerWords: ["Error", "in", "the", "call"] });
            this.setState({ loading: false })
            return;
        }
    }

    handleChange = (event) => {
        this.setState({ value: event.target.value });
    }

    handleClick = (e) => {
        e.preventDefault();
        console.log('The link was clicked.');
        this.setState({ value: e.target.innerText }, this.handleSubmit);
    }

    buildExamples = () => {
        return ["Qué se dice sobre futbol y politica?", "Qué se dice sobre el peronismo?"]
    }

    render() {
        return (
            <div className={styles.search}>
                <form className={styles.components} onSubmit={this.handleSubmit}>
                    <div className={styles.searchBar}>
                        <InputGroup >
                            <div className={styles.searchIcon}>
                                <i className="fa fa-search"></i>
                            </div>
                            <FormControl
                                placeholder="Buscar en episodios"
                                aria-label="Buscar en episodios"
                                aria-describedby="basic-addon2"
                                className={styles.searchInput}
                                onChange={this.handleChange}
                                value={this.state.value}
                            />
                        </InputGroup>
                    </div>
                </form >
                <div className={styles.examplesSection}>
                    <span className={styles.exampleTitle}>Ejemplos: </span><Examples examples={this.buildExamples()} handleClick={this.handleClick} />
                </div>
                <div className={styles.components}>
                    {this.state.loading ?
                        <div className={styles.spinner}>
                            <Spinner animation="border" role="status">
                                <span className="visually-hidden">Buscando...</span>
                            </Spinner>
                        </div>
                        : (
                            <div className={styles.responses}>
                                <div className={styles.answer}>
                                    <em>
                                        {this.state.answerWords.map((word, index) => (
                                            <span
                                                key={index}
                                                className={styles.fadeIn}
                                                style={{ animationDelay: `${index * 0.1}s` }}
                                            >
                                                {word}{" "}
                                            </span>
                                        ))}
                                    </em>
                                </div>
                                {this.state.sources.length > 0 &&
                                    <div className={styles.subtitle}>
                                        <h4>Episodios</h4>
                                    </div>}
                                {this.state.sources.map((source, index) => (
                                    <div key={index} className={styles.sources}>
                                        <Sources key={index} text={source.text} link={source.link} title={source.name} time={source.time} />
                                    </div>
                                ))}
                            </div>
                        )}
                </div>
            </div>
        );
    }
}

