import React from 'react';
import { Search } from '../search/search';
import styles from './hero.module.css';

export class Hero extends React.Component {

    constructor(props) {
        super(props);
        this.state = { query: "" };
    }

    render() {
        return (
            <div className={styles.hero}>
                <div className={styles.mainTitle}>
                    <h2>El metodo rebord</h2>
                    <p>Usa inteligencia artificial basada en ChatGPT para buscar episodios del Metodo Rebord</p>
                </div>
                <div className={styles.search}>
                    <Search />
                </div>
            </div >
        );
    }
}

