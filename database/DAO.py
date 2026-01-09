from database.DB_connect import DBConnect
from model.Constructor import Constructor
class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllConstructorsByYearRange(year1, year2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT DISTINCT c.constructorId, c.constructorRef, c.name, c.nationality
                FROM constructors c, results res, races r
                WHERE c.constructorId = res.constructorId
                  AND res.raceId = r.raceId
                  AND r.year BETWEEN %s AND %s
                  AND res.position IS NOT NULL
                ORDER BY c.constructorId"""
        cursor.execute(query, (year1, year2))

        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getConstructorEdges(year1, year2, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT res1.constructorId AS c1,
                    res2.constructorId AS c2,
                    COUNT(DISTINCT res1.driverId) AS weight
                    FROM results res1, results res2, races r1, races r2
                    WHERE res1.driverId = res2.driverId
                      AND res1.raceId = r1.raceId
                      AND res2.raceId = r2.raceId
                      AND res1.constructorId > res2.constructorId
                      AND r1.year BETWEEN %s AND %s
                      AND r2.year BETWEEN %s AND %s
                      AND res1.position IS NOT NULL
                      AND res2.position IS NOT NULL
                    GROUP BY res1.constructorId, res2.constructorId
                    ORDER BY weight DESC"""

        cursor.execute(query, (year1, year2, year1, year2))

        for row in cursor:
            results.append((idMap[row["c1"]], idMap[row["c2"]], row["weight"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getOldestDriverPerConstructor(year1, year2, idMap):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """SELECT res.constructorId, MIN(d.dob) AS oldest_driver_dob
                FROM results res, races r, drivers d
                WHERE res.raceId = r.raceId
                  AND res.driverId = d.driverId
                  AND r.year BETWEEN %s AND %s
                  AND res.position IS NOT NULL
                GROUP BY res.constructorId"""

        cursor.execute(query, (year1, year2))

        for row in cursor:
            if row["constructorId"] in idMap:
                idMap[row["constructorId"]].oldest_driver_dob = row["oldest_driver_dob"]

        cursor.close()
        conn.close()

