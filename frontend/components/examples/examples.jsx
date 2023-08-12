// React class based component that receives a list of words and creates Link components for each word

//Import necessary libraries
import React from 'react';
import Link from 'next/link';
import styles from './examples.module.css';


export class Examples extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className={styles.examples}>
                {this.props.examples.map((word, index) => (
                    <span key={index} className={styles.links}>
                        <Link
                            key={index}
                            href=""
                            onClick={this.props.handleClick}
                            className={styles.link}
                        >
                            {word}
                        </Link>
                    </span>
                ))}
            </div>
        );
    }
}
