-- Calculer le chiffre d'affaires total par jour du 1er janvier 2019 au 31 décembre 2019.
-- Il s'agit d'additionner le produit du prix et de la quantité (prod_prix * prod_quantité) pour chaque jour.

SELECT
    date,
    SUM(
        prod_price * prod_qty
        ) AS ventes
FROM
    TRANSACTIONS
WHERE
    date BETWEEN '2019-01-01' AND '2019-12-31'
GROUP BY
    date
ORDER BY
    date;
