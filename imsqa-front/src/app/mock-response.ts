import { Response, Entity, Answer } from './interfaces';

export const RESPONSE: Response = {
    question: 'who is the father of cryptography?',
    category: 'resource',
    types: ['dbo:Person',
            'dbo:Agent',
            'dbo:OfficeHolder',
            'dbo:MusicalArtist',
            'dbo:Writer',
            'dbo:Artist',
            'dbo:Athlete',
            'dbo:Company',
            'dbo:Organisation',
            'dbo:SoccerPlayer'
           ],
    entities: [
               {
                   rdfsComment: "[  Elliptic curve cryptography (ECC) is an approach to public-key cryptography based on the algebraic structure of elliptic curves over finite fields. One of the main benefits in comparison with non-ECC cryptography (with plain Galois fields as a basis) is the same level of security provided by keys of smaller size.Elliptic curves are applicable for encryption, digital signatures, pseudo-random generators and other tasks. @en]",
                   uri: "http://dbpedia.org/resource/Elliptic_curve_cryptography"
               },
               {
                   rdfsComment: "[  The following outline is provided as an overview of and topical guide to cryptography:Cryptography (or cryptology) – practice and study of hiding information. Modern cryptography intersects the disciplines of mathematics, computer science, and engineering. Applications of cryptography include ATM cards, computer passwords, and electronic commerce. @en]",
                   uri: "http://dbpedia.org/resource/Outline_of_cryptography"
               },
               {
                   rdfsComment: "[  A cryptographic hash function is a hash function which is considered practically impossible to invert, that is, to recreate the input data from its hash value alone. These one-way hash functions have been called \\ the workhorses of modern cryptography\\ . @en]",
                   uri: "http://dbpedia.org/resource/Cryptographic_hash_function"
               },
               {
                   rdfsComment: "[  Douglas Robert Stinson (born in 1956 in Guelph, Ontario) is a Canadian mathematician and cryptographer, currently a professor at the University of Waterloo and a member of the Centre for Applied Cryptographic Research.Stinson received his B.Math from the University of Waterloo in 1978, his MSc from Ohio State University in 1980, and his Ph.D. from the University of Waterloo in 1981. He was at the University of Manitoba from 1981 to 1989, and the University of Nebraska-Lincoln from 1990 to 1998. @en]",
                   uri: "http://dbpedia.org/resource/Doug_Stinson"
               },
               {
                   rdfsComment: "[  Father Brown is a British television period drama which began airing on BBC One on 14 January 2013. It features Mark Williams as the eponymous crime-solving Roman Catholic priest. The series is based on the character of Father Brown and some episodes are loosely inspired by original stories by G. K. Chesterton, primarily using new stories written for the series. @en]",
                   uri: "http://dbpedia.org/resource/Father_Brown_(2013_TV_series)"
               },
               {
                   rdfsComment: "[  In comparative mythology, sky father is a term for a recurring concept of a sky god who is addressed as a \\ father\\ , often the father of a pantheon. The concept of \\ sky father\\  may also be taken to include Sun gods with similar characteristics. The concept is complementary to an \\ earth mother\\ .\\ Sky Father\\  is a direct translation of the Vedic Dyaus Pita, etymologically identical to the Greek Zeus Pater. @en]",
                   uri: "http://dbpedia.org/resource/Sky_father"
               },
               {
                   rdfsComment: "[  The Name-of-the-Father (French Nom du père) is a concept that Jacques Lacan developed from his seminar The Psychoses (1955–1956) to cover the role of the father in the Symbolic Order. @en]",
                   uri: "http://dbpedia.org/resource/Name_of_the_Father"
               },
               {
                   rdfsComment: "[  Abinoam (a-bin'-o-am, ab-i-no'-am), from Kedesh-naphtali, was the father of Barak   who defeated Jabin's army, led by Sisera (Judges 4:6; 5:1).Meaning: father of beauty, father of kindness, father of pleasantness @en]",
                   uri: "http://dbpedia.org/resource/Abinoam"
               }
              ],
    answers: [
        {
            "answer": "http://dbpedia.org/resource/Nigel_Smart_(cryptographer)",
            "type": "http://dbpedia.org/ontology/Agent",
            "entity": "http://dbpedia.org/resource/Elliptic_curve_cryptography",
            "similarity": 0.5500500798225403
        },
        {
            "answer": "http://dbpedia.org/resource/Nigel_Smart_(cryptographer)",
            "type": "http://dbpedia.org/ontology/Person",
            "entity": "http://dbpedia.org/resource/Elliptic_curve_cryptography",
            "similarity": 0.5500500798225403
        },
        {
            "answer": "http://dbpedia.org/resource/Nigel_Smart_(cryptographer)",
            "type": "http://dbpedia.org/ontology/Scientist",
            "entity": "http://dbpedia.org/resource/Elliptic_curve_cryptography",
            "similarity": 0.5500500798225403
        },
        {
            "answer": "http://dbpedia.org/resource/Bart_Preneel",
            "type": "http://dbpedia.org/ontology/Agent",
            "entity": "http://dbpedia.org/resource/Cryptographic_hash_function",
            "similarity": 0.5500500798225403
        },
        {
            "answer": "http://dbpedia.org/resource/Bart_Preneel",
            "type": "http://dbpedia.org/ontology/Person",
            "entity": "http://dbpedia.org/resource/Cryptographic_hash_function",
            "similarity": 0.5500500798225403
        },
        {
            "answer": "http://dbpedia.org/resource/Bart_Preneel",
            "type": "http://dbpedia.org/ontology/Scientist",
            "entity": "http://dbpedia.org/resource/Cryptographic_hash_function",
            "similarity": 0.5500500798225403
        },
        {
            "answer": "http://dbpedia.org/resource/Paulo_S._L._M._Barreto",
            "type": "http://dbpedia.org/ontology/Agent",
            "entity": "http://dbpedia.org/resource/Cryptographic_hash_function",
            "similarity": 0.5500500798225403
        },
        {
            "answer": "http://dbpedia.org/resource/Paulo_S._L._M._Barreto",
            "type": "http://dbpedia.org/ontology/Person",
            "entity": "http://dbpedia.org/resource/Cryptographic_hash_function",
            "similarity": 0.5500500798225403
        },
        {
            "answer": "http://dbpedia.org/resource/Paulo_S._L._M._Barreto",
            "type": "http://dbpedia.org/ontology/Scientist",
            "entity": "http://dbpedia.org/resource/Cryptographic_hash_function",
            "similarity": 0.5500500798225403
        },
        {
            "answer": "http://dbpedia.org/resource/Souradyuti_Paul",
            "type": "http://dbpedia.org/ontology/Agent",
            "entity": "http://dbpedia.org/resource/Cryptographic_hash_function",
            "similarity": 0.5500500798225403
        }]
};